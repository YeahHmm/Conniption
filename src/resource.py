from collections import deque
from copy import deepcopy
from itertools import repeat, chain
import os


class Move:
    action = {'flip':'flip', 'place':'place', 'none':'none'}
    
    def __init__(self, act_key='none', player=0, column=-1):
        self._action = Move.action[act_key]
        self._player = player
        self._column = column

    def toTupple(self):
        return (self._player, self._action, self._column)

    def __eq__(self, mv):
        return self.toTupple() == mv.toTupple()

    def __hash__(self):
        return self.toTupple().__hash__()


class SystemState:
    def __init__(self, board=list(repeat(deque(), 7)), prev_move=Move(), \
            cur_player=1, num_flips=(0, 0), is_down=0):
        self._board = board
        self._prev_move = prev_move
        self._cur_player = cur_player
        self._num_flips = num_flips
        self._is_down = is_down

    def update(self, mv):
        new_board = deepcopy(self._board)
        new_player = self._cur_player * -1
        new_flips = deepcopy(self._num_flips)
        new_down = self._is_down
        
        if mv._action == Move.action['flip']:
            new_flips = tuple(map(lambda i: new_flips[i] + (i == self._cur_player), range(2)))
            new_down = not new_down
        elif mv._action == Move.action['place']:
            if self._is_down:
                new_board[mv._column].append(self._cur_player)
            else:
                new_board[mv._column].appendLeft(self._cur_player)

        return SystemState(new_board, mv, new_player, new_flips, new_down)

    def validMove(self, mv):
        return False

    def isGoal(self):
        return False

    def toTupple(self):
        boardTup = tuple(map(tuple, self._board))
        return (boardTup, self._prev_move, self._cur_player, self._num_flips, self._is_up)

    def __eq__(self, state):
        return self.toTupple() == state.toTupple()

    def __hash__(self):
        return self.toTupple().__hash__()

    def __repr__(self):
        return self.toTupple().__repr__()

    def __str__(self):
        os.system('clear')
        matrix = list(chain.from_iterable(self._board))
        toPrint = ' ' + '----' * 14 + '\n|'
        #toPrint += '|'
        for i, j in enumerate(matrix):
            toPrint += '{0:^7}|'.format(j)
            if i % 7 == 6:
                toPrint += '\n'
                toPrint += ' ' + '----' * 14 + '\n|'
        toPrint = toPrint[:-1]
        return toPrint
