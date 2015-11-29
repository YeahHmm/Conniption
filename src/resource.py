from copy import deepcopy, copy
from itertools import repeat, product, combinations
from termcolor import colored
import os

import const
from graph import Graph

class Node:
    def __init__(self, value, item):
        self._value = value
        self._item = item

    def __eq__(self, nd):
        return self._value == nd._value
    
    def __lt__(self, nd):
        return self._value < nd._value

    def __repr__(self):
        return str((self._value, self._item))


class Move:
    action = ['flip', 'place', 'none']

    def __init__(self, action='none', player=-1, column=-1):
        self._action = action
        self._player = player
        self._column = column

    def toTuple(self):
        return (self._action, self._player, self._column)

    def __eq__(self, mv):
        return self.toTuple() == mv.toTuple()

    def __hash__(self):
        return self.toTuple().__hash__()

    def __repr__(self):
        return self.toTuple().__str__()


class SystemState:
    def __init__(self, board=list(repeat([], 7)), prev_move=Move(), \
            player=0, num_flips=(0, 0), is_down=0, stage=0, num_placed=0):
        self._board = board
        self._prev_move = prev_move
        self._player = player
        self._num_flips = num_flips
        self._is_down = is_down
        self._stage = stage
        self._num_placed = 0

    def update(self, mv):
        new_board = deepcopy(self._board)
        new_player = self._player
        new_flips = deepcopy(self._num_flips)
        new_down = self._is_down
        new_stage = (self._stage + 1) % 3
        new_placed = self._num_placed

        if mv._action == 'flip':
            if self._prev_move._player == mv._player:
                new_player = int(not new_player)
            new_flips = tuple(map(lambda i: new_flips[i] + (i == self._player), range(2)))
            new_down = int(not new_down)
        elif mv._action == 'place':
            new_placed += 1
            if self._is_down:
                new_board[mv._column] = [self._player] + new_board[mv._column]
            else:
                new_board[mv._column] = new_board[mv._column] + [self._player]
        elif mv._action == 'none':
            if self._prev_move._player == mv._player:
                new_player = int(not new_player)

        return SystemState(new_board, mv, new_player, new_flips, new_down, \
                new_stage, new_placed)

    def validMove(self, mv):
        if self._player != mv._player:
            return False

        if mv._action == 'flip' and self._num_flips[mv._player] >= const.MAX_FLIPS:
            return False

        if mv._player == self._prev_move._player:
            if self._prev_move._action != 'place':
                if mv._action == 'place':
                    return True

        if self._prev_move._action != 'flip':
            return mv._action != 'place'
        else:
            return mv._action == 'none'
        
        return False

    def genMoves(self):
        moves = set()

        if self._player == self._prev_move._player:
            if self._prev_move._action == 'flip' or self._prev_move._action == 'none':
                for i in range(const.NUM_COLS):
                    if len(self._board[i]) < const.NUM_ROWS:
                        moves.add(Move('place', self._player, i))
                return moves

        if self._prev_move._action != 'flip':
            if self._num_flips[self._player] < const.MAX_FLIPS:
                moves.add(Move('flip', self._player))
            moves.add(Move('none', self._player))
        else:
            moves.add(Move('none', self._player))

        return moves

    def isGoal(self, check_none=False):
        if self._prev_move._action == 'flip':
            return self._isGoal_flip()
        elif self._prev_move._action == 'place':
            return self._new_isGoal_place()
        elif self._prev_move._action == 'none' and check_none:
            return self._isGoal_flip()

        return (False, const.EMPTY_VAL)

    # Rewrite to check for draws
    def _isGoal_flip(self):
        slen = const.LEN_SOL
        sgraph = const.SOLS_GRAPH
        sdict = {s : True for s in sgraph.getVertices()}
        board = self.filledMatrix()
        player = self._prev_move._player

        win_sols = set()
        lose_sols = set()
        for sol in sdict:
            if not sdict[sol]:
                continue

            vals_win = list(filter(lambda p: board[p[0]][p[1]] == player, sol))
            vals_lose = filter(lambda p: board[p[0]][p[1]] == int(not player), sol)
            vals_lose = list(vals_lose)
            vals_none = filter(lambda p: board[p[0]][p[1]] == const.EMPTY_VAL, sol)

            if len(vals_win) == slen:
                win_sols.add(sol)
                #return (True, self._player)
            elif len(vals_lose) == slen:
                lose_sols.add(sol)
                #return (True, int(not self._player))

            for cell in vals_none:
                for s in sgraph.neighbors(sol, (cell,)):
                    sdict[s] = False

            for pair in map(lambda p: tuple(sorted(p)), product(vals_win, vals_lose)):
                for s in sgraph.neighbors(sol, pair):
                    sdict[s] = False

        if len(win_sols) > 0:
            return (True, player)
        elif len(lose_sols) > 0:
            return (True, int(not player))
        elif self._num_placed == const.NUM_COLS * const.NUM_ROWS and \
                self._stage == const.NUM_STAGES-1:
            return (True, const.EMPTY_VAL)
        else:
            return (False, const.EMPTY_VAL)

    def _new_isGoal_place(self):
        matrix = self.filledMatrix()
        col = self._prev_move._column
        row = len(self._board[col])-1

        for sol in const.CELL_MAP[(col, row)]:
            ls = filter(lambda p: matrix[p[0]][p[1]] == self._player, sol)
            if len(list(ls)) == const.LEN_SOL:
                return (True, self._player)

        if self._num_placed == const.NUM_COLS * const.NUM_ROWS and \
                self._stage == const.NUM_STAGES-1:
            return (True, const.EMPTY_VAL)

        return (False, const.EMPTY_VAL)

    def _isGoal_place(self):
        row = len(self._board[self._prev_move._column])-1
        matrix = deepcopy(self.filledMatrix())
        col = copy(self._prev_move._column)

        if matrix[col][row] != 2: #Avoid test in case of none or flip moves
            # Horizontal
            i = col - 3 if col > 3 else 0
            while i <= col and i <= const.NUM_COLS-4:
                if matrix[i][row]==matrix[i+1][row]==matrix[i+2][row]==matrix[i+3][row]:
                    return True, self._player
                i += 1
            # Vertical
            j = row - 3 if row > 3 else 0
            while j <= row and j <= const.NUM_ROWS-4:
                if matrix[col][j]==matrix[col][j+1]==matrix[col][j+2]==matrix[col][j+3]:
                    return True, self._player
                j += 1
            # Diagonal Left to rigth down
            startCol = col - 3 if col > 3 else 0
            #startRow = row + 3 if col > 3 else row + col
            startRow = row + col - startCol
            while startCol <= col and startCol < 4:
                if startRow > 2 and startRow < 6:
                    if matrix[startCol][startRow]==matrix[startCol+1][startRow-1]\
                    ==matrix[startCol+2][startRow-2]==matrix[startCol+3][startRow-3]:
                        return True, self._player
                startCol += 1
                startRow -= 1
            # Diagonal left to Right up
            startCol = col - 3 if col > 3 else 0
            #startRow = row - 3 if col > 3 else row - col
            startRow = row - 3 if col > 3 else row - col + startCol
            while startCol <= col and startCol < 4:
                if startRow >= 0 and startRow < 4:
                    if matrix[startCol][startRow]==matrix[startCol+1][startRow+1]\
                    ==matrix[startCol+2][startRow+2]==matrix[startCol+3][startRow+3]:
                        return True, self._player
                startCol += 1
                startRow += 1

        return False, 2

    def isGoalFlipped(self):
        matrix = deepcopy(self.filledMatrix())
        for j in range(const.NUM_ROWS):
            for i in range(const.NUM_COLS):
                col = i
                row = j
                if matrix[col][row] != 2: #Avoid test in case of none or flip moves
                    # Horizontal
                    i = col - 3 if col > 3 else 0
                    while i <= col and i <= const.NUM_COLS-4:
                        if matrix[i][row]==matrix[i+1][row]==matrix[i+2][row]==matrix[i+3][row]:
                            return True, self._player
                        i += 1
                    # Vertical
                    j = row - 3 if (row%7) > 3 else 0
                    while j <= row and j <= const.NUM_ROWS-4:
                        if matrix[col][j]==matrix[col][j+1]==matrix[col][j+2]==matrix[col][j+3]:
                            return True, self._player
                        j += 1
                    # Diagonal Left to rigth down
                    startCol = col - 3 if col > 3 else 0
                    startRow = row + 3 if col > 3 else row + col
                    while startCol <= col and startCol <= 3:
                        if startRow > 2 and startRow <6:
                            if matrix[startCol][startRow]==matrix[startCol+1][startRow-1]\
                            ==matrix[startCol+2][startRow-2]==matrix[startCol+3][startRow-3]:
                                return True, self._player
                        startCol += 1
                        startRow -= 1
                    # Diagonal left to Right up
                    startCol = col - 3 if col > 3 else 0
                    startRow = row - 3 if col > 3 else row - col
                    while startCol <= col and startCol <= 3:
                        if startRow >= 0 and startRow <4:
                            if matrix[startCol][startRow]==matrix[startCol+1][startRow+1]\
                            ==matrix[startCol+2][startRow+2]==matrix[startCol+3][startRow+3]:
                                return True, self._player
                        startCol += 1
                        startRow += 1
        return False, 2


    def filledMatrix(self):
        e = const.EMPTY_VAL
        if self._is_down:
            filled = list(map(lambda c: c[::-1] + [e]*(const.NUM_ROWS - len(c)), self._board))
        else:
            filled = list(map(lambda c: c + [e]*(const.NUM_ROWS - len(c)), self._board))
        return filled

    def getBoardTuple(self):
        return tuple(map(tuple, self._board))

    def toTuple(self):
        boardTup = self.getBoardTuple()
        return (boardTup, self._prev_move, self._player, self._num_flips, self._is_down)

    def __eq__(self, state):
        return self.getBoardTuple() == state.getBoardTuple()

    def __hash__(self):
        return self.getBoardTuple().__hash__()

    def __repr__(self):
        return self.toTuple().__repr__()

    def __str__(self):
        filled = self.filledMatrix()
        filled = list(zip(*filled))[::-1]
        conv = lambda k: 'X' if k == 0 else 'O' if k == 1 else ' '
        filled = list(map(lambda c: list(map(conv, c)), filled))

        toPrint = colored(' ' + '----' * 14 + '\n|', 'yellow')
        for i in range(const.NUM_ROWS):
            for j in range(const.NUM_COLS):
                if '{0:^7}'.format(filled[i][j]) == '   X   ':
                    toPrint += colored('{0:^7}'.format(filled[i][j]),'cyan', 'on_cyan')
                elif '{0:^7}'.format(filled[i][j]) == '   O   ':
                    toPrint += colored('{0:^7}'.format(filled[i][j]),'white', 'on_white')
                else:
                    toPrint += '{0:^7}'.format(filled[i][j])
                toPrint += colored('|', 'yellow')

                if j % const.NUM_COLS == const.NUM_COLS - 1:
                    toPrint += '\n'
                    toPrint += colored(' ' + '----' * 14 + '\n|', 'yellow')
        toPrint = toPrint[:-6]

        return toPrint

    @staticmethod
    def _buildSols():
        ncols = const.NUM_COLS
        nrows = const.NUM_ROWS
        slen = const.LEN_SOL

        sols_graph = Graph()
        chain_dict = {}

        vert_i = range(ncols - (slen - 1))
        vert_j = range(nrows)
        vert_start = product(vert_i, vert_j)
        for i, j in vert_start:
            xlist = range(i, i + slen)
            chain = tuple((x, j) for x in xlist)
            sols_graph.addVertex(chain)

        horiz_i = range(ncols)
        horiz_j = range(nrows - (slen - 1))
        horiz_start = product(horiz_i, horiz_j)
        for i, j in horiz_start:
            ylist = range(j, j + slen)
            chain = tuple((i, y) for y in ylist)
            sols_graph.addVertex(chain)

        ldiag_i = range(ncols - (slen - 1))
        ldiag_j = range(nrows - (slen - 1))
        ldiag_start = product(ldiag_i, ldiag_j)
        for i, j in ldiag_start:
            xlist = range(i, i + slen)
            ylist = range(j, j + slen)
            chain = tuple((x, y) for x, y in zip(xlist, ylist))
            sols_graph.addVertex(chain)

        rdiag_i = range(slen - 1, ncols)
        rdiag_j = range(nrows - (slen - 1))
        rdiag_start = product(rdiag_i, rdiag_j)
        for i, j in rdiag_start:
            xlist = range(i, i - slen - 1, -1)
            ylist = range(j, j + slen)
            chain = tuple((x, y) for x, y in zip(xlist, ylist))
            sols_graph.addVertex(chain)

        for chain in sols_graph.getVertices():
            keys = set()
            for i in range(1, slen - 1):
                keys.update(combinations(chain[1:], i))
                keys.update(combinations(chain[:3], i))
            for k in keys:
                if k not in chain_dict:
                    chain_dict[k] = set()
                chain_dict[k].add(chain)

        for k in chain_dict:
            for chain in chain_dict[k]:
                for c in chain_dict[k]:
                    if c is chain:
                        continue
                    sols_graph.addEdge(chain, c, k)

                    for p in c:
                        if p not in const.CELL_MAP:
                            const.CELL_MAP[p] = set()
                        const.CELL_MAP[p].add(c)

        const.SOLS_GRAPH = sols_graph


SystemState._buildSols()
