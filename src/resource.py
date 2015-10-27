from copy import deepcopy
from itertools import repeat, chain
import os


class Move:
    action = {'flip':'flip', 'place':'place', 'none':'none'}

    def __init__(self, action='none', player=0, column=-1):
        self._action = action
        self._player = player
        self._column = column

    def toTupple(self):
        return (self._player, self._action, self._column)

    def __eq__(self, mv):
        return self.toTupple() == mv.toTupple()

    def __hash__(self):
        return self.toTupple().__hash__()


class SystemState:
    def __init__(self, board=list(repeat([0,0,0,0,0,0], 7)), prev_move=Move(), \
            cur_player=0, num_flips=(0, 0), is_up=0):
        self._board = board
        self._prev_move = prev_move
        self._cur_player = cur_player
        self._num_flips = num_flips
        self._is_up = is_up

    def update(self, mv):
        new_player = not self._cur_player
        new_board = deepcopy(self._board)

        if mv._action == Move.action['flip']:
            new_up = not self._is_up
            #new_num_flips =
            pass
        elif mv._action == Move.action['place']:
            pass
        elif mv._action == Move.action['none']:
            pass

        return

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

    def __str__(self):
        os.system('clear')
        matrix = list(chain.from_iterable(self._board))
        toPrint = ' ' + '----' * 14 + '\n|'
        #toPrint += '|'
        for i, j in enumerate(matrix):
            toPrint += '{0:^7}|'.format(j)
            if i == 6 or i == 13 or i == 20 or i ==27 or i == 34\
               or i ==41:
                toPrint += '\n'
                toPrint += ' ' + '----' * 14 + '\n|'
        toPrint = toPrint[:-1]
        return toPrint
