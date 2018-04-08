from copy import deepcopy, copy
from itertools import repeat, product, combinations
from termcolor import colored
import os
import numpy as np

from resources import const
from resources.graph import Graph

'''
A class for sorting items by arbitrary keys such as values output by an
evaluation function.
'''
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


'''
Separate moves into three types: flip, place, and none.
The none type refers to a move where the player neither flipped nor placed.

A ply consists of three of these moves, two being none or flip and one being
a place.
'''
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



'''
Records the current state of the game for use in the main game loop and in
AI searching functions. Updating with a Move occurs immutably.
'''
class SystemState:
    def __init__(self, board=list(repeat([], 7)), prev_move=Move(), \
            player=0, num_flips=(0, 0), is_down=0, stage=0, num_placed=0):
        self._board = board
        self._prev_move = prev_move
        self._player = player
        self._num_flips = num_flips
        self._is_down = is_down
        self._stage = stage
        self._num_placed = num_placed

    '''
    Accepts a Move object and creates a new SystemState based upon that Move.
    Using this function enforces immutability of SystemState objects.
    This function assumes the Move is legal.
    '''
    def update(self, mv):
        new_board = deepcopy(self._board)
        new_player = self._player
        new_flips = deepcopy(self._num_flips)
        new_down = self._is_down
        new_stage = (self._stage + 1) % 3
        new_placed = self._num_placed

        # Toggle _is_down and decrement player's flips. Swap _player if end
        # of turn
        if mv._action == 'flip':
            if self._prev_move._player == mv._player:
                new_player = int(not new_player)
            new_flips = tuple(map(lambda i: new_flips[i] + (i == self._player), \
                range(2)))
            new_down = int(not new_down)
        # Increment num_placed and place tile in correct position
        elif mv._action == 'place':
            new_placed += 1
            if self._is_down:
                new_board[mv._column] = [self._player] + new_board[mv._column]
            else:
                new_board[mv._column] = new_board[mv._column] + [self._player]
        # Swap _player if end of turn
        elif mv._action == 'none':
            if self._prev_move._player == mv._player:
                new_player = int(not new_player)

        return SystemState(new_board, mv, new_player, new_flips, new_down, \
                new_stage, new_placed)

    '''
    Accepts a Move object and outputs True if it is legal for this
    SystemState. This enforces the rules for the number of flips, ordering of
    Move types, and whether the Move is for the correct player.
    '''
    def validMove(self, mv):
        # Move must be for the correct player
        if self._player != mv._player:
            return False

        # Cannot flip if no flips remaining
        if mv._action == 'flip' and self._num_flips[mv._player] >= const.MAX_FLIPS:
            return False

        # Only option in middle of turn is Place
        if mv._player == self._prev_move._player:
            if self._prev_move._action != 'place':
                if mv._action == 'place':
                    return True

        # Can flip or do nothing if in 1st or 3rd stage and prevous Move was
        # not a flip
        if self._prev_move._action != 'flip':
            return mv._action != 'place'
        # Cannot flip twice in a row
        else:
            return mv._action == 'none'

        return False

    '''
    Uses similar logic to validMove() to generate the list of currently legal
    Move objects.
    '''
    def genMoves(self):
        moves = set()

        # If in 2nd stage, return place Moves to unfilled columns
        if self._player == self._prev_move._player:
            if self._prev_move._action == 'flip' or self._prev_move._action == 'none':
                for i in range(const.NUM_COLS):
                    if len(self._board[i]) < const.NUM_ROWS:
                        moves.add(Move('place', self._player, i))
                return moves

        # If in 1st or 3rd stage, return flip and none Moves if previous Move
        # was not a flip
        if self._prev_move._action != 'flip':
            moves.add(Move('none', self._player))
            if self._num_flips[self._player] < const.MAX_FLIPS:
                moves.add(Move('flip', self._player))
        # Otherwise only return none Move
        else:
            moves.add(Move('none', self._player))

        return moves

    def legal_moves(self):
        return list(sorted(list(self.genMoves()), key= lambda x: x._column))

    '''
    Parent function for identifying the end of a game. Delegates the
    verification to other functions based upon the previous move that was
    made, checks for a draw if no function is chosen, and defaults to False.

    Output is a tuple (gameEnd, winner), recording whether the game is over
    and if there was a winner. The two separate values are necessary for draws
    where the game ends, but there is no winner. The winner variable is an
    integer 0, 1, or const.EMPTY_VAL corresponding to Player 1, Player 2, and
    No-Winner respectively.
    '''
    def isGoal(self, check_none=False):
        val = (False, const.EMPTY_VAL)

        if self._prev_move._action == 'flip':
            val = self._isGoal_flip()
        elif self._prev_move._action == 'place':
            # Draws occur when a player must place with no positions left
            if self._isDraw():
                val = (True, const.EMPTY_VAL)
            else:
                val = self._isGoal_place()
        elif self._prev_move._action == 'none' and check_none:
            val = self._isGoal_flip()

        return val

    def done(self):
        return self.isGoal()
    '''
    A draw occurs when all cells are filled, and the player must place a tile.
    '''
    def _isDraw(self):
        return self._num_placed == const.NUM_COLS * const.NUM_ROWS

    '''
    Function primarily responsible for finding winning flips. This function
    searches the entire board with a graph for optimization. Note that this
    function also enforces the flipping rule where ties are broken by the
    player who flipped.
    '''
    def _isGoal_flip(self):
        slen = const.LEN_SOL
        sgraph = const.SOLS_GRAPH
        sdict = {s : True for s in sgraph.getVertices()}
        board = self.filledMatrix()
        player = self._prev_move._player

        win_sols = set()
        lose_sols = set()
        for sol in sdict:
            # Ignore flagged solutions
            if not sdict[sol]:
                continue

            # Separate solution's cells into those belonging to this player,
            # those belonging to the other, and those that are empty
            vals_win = list(filter(lambda p: board[p[0]][p[1]] == player, sol))
            vals_lose = filter(lambda p: board[p[0]][p[1]] == int(not player), sol)
            vals_lose = list(vals_lose)
            vals_none = filter(lambda p: board[p[0]][p[1]] == const.EMPTY_VAL, sol)

            # This player wins if a solution has `slen` of his tiles in it
            if len(vals_win) == slen:
                win_sols.add(sol)
            # The other player wins if a solution `slen` of his tiles in it
            elif len(vals_lose) == slen:
                lose_sols.add(sol)

            # Flag all solutions containing each unfilled cell
            for cell in vals_none:
                for s in sgraph.neighbors(sol, (cell,)):
                    sdict[s] = False

            # Flag all solutions containing two different tiles
            for pair in map(lambda p: tuple(sorted(p)), product(vals_win, vals_lose)):
                for s in sgraph.neighbors(sol, pair):
                    sdict[s] = False

        # If this player has filled a solution, he wins with priority
        if len(win_sols) > 0:
            return (True, player)
        # Otherwise, if the other player has filled a solution, he wins
        elif len(lose_sols) > 0:
            return (True, int(not player))
        # Otherwise, continue playing
        else:
            return (False, const.EMPTY_VAL)

    '''
    Function primarily responsible for finding winning placements. This
    function only searches the neighborhood of the previously placed tile.
    '''
    def _isGoal_place(self):
        matrix = self.filledMatrix()
        col = self._prev_move._column
        row = len(self._board[col])-1

        # Search all solutions containing the previously filled cell.
        # Return a win if this player created a winning solution.
        # A player cannot place a tile and create a losing solution.
        for sol in const.CELL_MAP[(col, row)]:
            ls = filter(lambda p: matrix[p[0]][p[1]] == self._player, sol)
            if len(list(ls)) == const.LEN_SOL:
                return (True, self._player)


        return (False, const.EMPTY_VAL)

    '''
    Convert the board data structure to a full grid. This grid must be
    transposed prior to printing.
    '''
    def filledMatrix(self):
        e = const.EMPTY_VAL
        # Reverse column and place empty cells if board is flipped
        if self._is_down:
            filled = list(map(lambda c: c[::-1] + [e]*(const.NUM_ROWS - len(c)), self._board))
        # Otherwise, simply place empty cells
        else:
            filled = list(map(lambda c: c + [e]*(const.NUM_ROWS - len(c)), self._board))
        return filled

    def getBoardTuple(self):
        return tuple(map(tuple, self._board))

    '''
        Necessary methods for the AlphaZero implementation
    '''

    def black_and_white_plane(self):
        filled = self.filledMatrix()
        board = list(zip(*filled))[::-1]
        board_white = np.copy(board)
        board_black = np.copy(board)
        for i in range(6):
            for j in range(7):
                if board[i][j] == 2:
                    board_white[i][j] = 0
                    board_black[i][j] = 0
                elif board[i][j] == 1:
                    board_white[i][j] = 1
                    board_black[i][j] = 0
                else:
                    board_white[i][j] = 0
                    board_black[i][j] = 1
        return np.array(board_white), np.array(board_black)

    def player_turn(self):
        return self._player

    @property
    def observation(self):
        filled = self.filledMatrix()
        board = list(zip(*filled))[::-1]
        return ''.join(''.join(str(x) for x in y) for y in board)

    def toTuple(self):
        boardTup = self.getBoardTuple()
        return (boardTup, self._prev_move, self._player, self._num_flips, self._is_down)

    def __eq__(self, state):
        return self.getBoardTuple() == state.getBoardTuple()

    def __hash__(self):
        return (self.getBoardTuple(), self._stage, self._num_flips, self._is_down).__hash__()

    def __repr__(self):
        return self.toTuple().__repr__()

    # Convert board to printable string for use in CLI
    def __str__(self):
        # Get filled board and transpose for display
        filled = self.filledMatrix()
        filled = list(zip(*filled))[::-1]

        # Map cells to X's, O's and spaces depending on tiles placed
        conv = lambda k: 'X' if k == 0 else 'O' if k == 1 else ' '
        filled = list(map(lambda c: list(map(conv, c)), filled))

        # Construct formatted and colored board. Colors are based on previous
        # mapping
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

    '''
    Construct the data structures used by isGoal() and evaluation functions
    for optimized searching.

    const.SOLS_GRAPH is a graph with solution
    coordinates as nodes and adjacencies drawn between solutions that share
    cells or pairs of cells.

    const.
    '''
    @staticmethod
    def _buildSols():
        ncols = const.NUM_COLS
        nrows = const.NUM_ROWS
        slen = const.LEN_SOL

        sols_graph = Graph()
        chain_dict = {}

        # Generate vertical solutions
        vert_i = range(ncols - (slen - 1))
        vert_j = range(nrows)
        vert_start = product(vert_i, vert_j)
        for i, j in vert_start:
            xlist = range(i, i + slen)
            chain = tuple((x, j) for x in xlist)
            sols_graph.addVertex(chain)

        # Generate horizontal solutions
        horiz_i = range(ncols)
        horiz_j = range(nrows - (slen - 1))
        horiz_start = product(horiz_i, horiz_j)
        for i, j in horiz_start:
            ylist = range(j, j + slen)
            chain = tuple((i, y) for y in ylist)
            sols_graph.addVertex(chain)

        # Generate solutions along y = -x (might be other direction)
        ldiag_i = range(ncols - (slen - 1))
        ldiag_j = range(nrows - (slen - 1))
        ldiag_start = product(ldiag_i, ldiag_j)
        for i, j in ldiag_start:
            xlist = range(i, i + slen)
            ylist = range(j, j + slen)
            chain = tuple((x, y) for x, y in zip(xlist, ylist))
            sols_graph.addVertex(chain)

        # Generate solutions along y = x (might be other direction)
        rdiag_i = range(slen - 1, ncols)
        rdiag_j = range(nrows - (slen - 1))
        rdiag_start = product(rdiag_i, rdiag_j)
        for i, j in rdiag_start:
            xlist = range(i, i - slen - 1, -1)
            ylist = range(j, j + slen)
            chain = tuple((x, y) for x, y in zip(xlist, ylist))
            sols_graph.addVertex(chain)

        # Create a mapping between cells and cell pairs to sets of solutions
        for chain in sols_graph.getVertices():
            keys = set()
            for i in range(1, slen - 1):
                keys.update(combinations(chain[1:], i))
                keys.update(combinations(chain[:3], i))
            for k in keys:
                if k not in chain_dict:
                    chain_dict[k] = set()
                chain_dict[k].add(chain)

        # Iterate over the cells and cell pairs to construct SOLS_GRAPH and
        # CELL_MAP
        for k in chain_dict:
            for chain in chain_dict[k]:
                for c in chain_dict[k]:
                    if c is chain:
                        continue
                    # Add graph edges between solutions in the same set
                    sols_graph.addEdge(chain, c, k)

                    # Add a solution to the CELL_MAP set corresponding to
                    # each of the cells in the edge
                    for p in c:
                        if p not in const.CELL_MAP:
                            const.CELL_MAP[p] = set()
                        const.CELL_MAP[p].add(c)

        const.SOLS_GRAPH = sols_graph


SystemState._buildSols()
