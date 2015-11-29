from collections import deque
import heapq
import os
import pickle
import random
import sys

from termcolor import colored
from getch import _Getch

import const

from printing import prompt
from resource import Node, Move, SystemState

class Game:
    def __init__(self, player_pair):
        self._state = SystemState()
        self._player_pair = player_pair
        self._history = []
        self._winner = None
        self._gameEnd = False

    def getState(self):
        return self._state

    def getCurPlayer(self):
        return self._player_pair[self._state._player]

    def update(self, mv):
        self._state = self._state.update(mv)
        self._history.append(mv)

    def checkWin(self):
        self._gameEnd, winner = self._state.isGoal()
        if self._gameEnd and winner != const.EMPTY_VAL:
            self._winner = self._player_pair[winner]

        return self._gameEnd

    def save(self, fname):
        pair = self._player_pair
        if os.path.isfile(fname):
            data = pickle.load(open(fname, 'rn'))
        else:
            data = []

        players = (pair[0]._name, pair[1]._name)
        win_state = (self._gameEnd, self._winner._name)
        mv_list = tuple(self._history)

        game = (players, win_state, mv_list)
        data.append(game)

        f = open(fname, 'wb')
        pickle.dump(data, f)

    def log(self, fname):
        pair = self._player_pair
        f = open(fname, 'a')

        line = ''
        line += str((pair[0]._name, pair[1]._name))
        line += ',' + str((self._gameEnd, self._winner._name))
        line += ',' + str(self._history)

        f.write(line + "\n")
        f.close()

    def drawScreen(self, msg=''):
        if not const.DEBUG:
            os.system('clear')
        toPrint = ' '
        for i in range(const.NUM_COLS):
            toPrint += '{0:^7} '.format(i+1)
        print(toPrint)
        print(self._state)

        p1 = self._player_pair[0]
        flip1 = ' '.join('*' * (const.MAX_FLIPS - self._state._num_flips[0]))
        space1 = ' ' * (20 - len(str(p1)) - len(flip1))

        p2 = self._player_pair[1]
        flip2 = ' '.join('*' * (const.MAX_FLIPS - self._state._num_flips[1]))
        space2 = ' ' * (20 - len(str(p2)) - len(flip2))

        print(colored(str(p1), 'cyan') + space1 + colored(flip1, 'green', attrs=['bold']))
        print(colored(str(p2), 'white') + space2 + colored(flip2, 'green', attrs=['bold']))

        print()

        stage = 'Place' if self._state._stage == 1 else 'Flip'
        print(str(self.getCurPlayer()) + "'s turn: %s Stage " % stage)
        if msg != '':
            print(msg)


class Player:
    def __init__(self, name):
        self._name = name

    def toTuple(self):
        return (self._name,)

    def __eq__(self, other):
        return self.toTuple() == other.toTuple()

    def __hash__(self):
        return self.toTuple().__hash__()

    def __repr__(self):
        return self.toTuple().__repr__()

    def __str__(self):
        return str(self._name)

    def choose_move(self, state):
        pass


class Human(Player):
    def choose_move(self, state):
        mv = None
        while not mv or not state.validMove(mv):
            if state._stage == 0 or state._stage == 2:
                if state._prev_move._action != 'flip' and \
                        state._num_flips[state._player] < const.MAX_FLIPS:
                    msg = 'Flip or Pass [f or p]:'
                    mapping = {'f':'flip', 'p':'none'}
                else:
                    mv = Move('none', state._player)
                    break
            elif state._stage == 1:
                msg = 'Place [1-%d]:' % (const.NUM_COLS + 1)
                mapping = {str(n) : 'place' for n in range(1, const.NUM_COLS + 1)}

            sys.stdout.flush()
            key = prompt(msg).lower()
            if key in mapping:
                if key.isnumeric():
                    mv = Move(mapping[key], state._player, int(key)-1)
                else:
                    mv = Move(mapping[key], state._player)

        return mv


class AI(Player):
    def __init__(self, name, evalFunc, max_depth=1, tieChoice=None):
        self.evalFunc = evalFunc
        self.tieChoice = tieChoice
        self._max_depth = max_depth
        super().__init__(name)

    def choose_move(self, state):
        mv = self._minimax(state, state._player == 0)
        return mv

    def toTuple(self):
        return (self._name, self.evalFunc)

    def _minimax(self, base_state, get_max):
        mv_list = base_state.genMoves()

        # Data for next recursion
        cmod = base_state._stage == const.NUM_STAGES - 1
        new_choice = cmod ^ get_max
        new_depth = new_choice != get_max

        children = []
        for mv in mv_list:
            new_state = base_state.update(mv)
            tup = new_state.getBoardTuple()
            mv_val = self._minimax_help(new_state, new_depth, \
                    new_choice, get_max)

            children.append(Node(mv_val, mv))

        if self.tieChoice is not None:
            return self.tieChoice(children, get_max)
        else:
            return AI.tieChoice_random(children, get_max)

    def _minimax_help(self, base_state, depth, get_max, init_choice,
            alpha=None, beta=None):
        if depth > self._max_depth and base_state._stage == 0:
            val = self.evalFunc(base_state)
            return val

        if base_state.isGoal()[0]:
            val = self.evalFunc(base_state)
            return val

        # Data for next recursion
        cmod = base_state._stage == const.NUM_STAGES - 1
        new_choice = cmod ^ get_max
        new_depth = depth + (new_choice != init_choice)

        choice_func = max if get_max else min
        mv_list = base_state.genMoves()
        best = None
        for mv in mv_list:
            new_state = base_state.update(mv)
            val = self._minimax_help(new_state, new_depth, \
                    new_choice, init_choice, alpha, beta)

            if best == None:
                best = val
            elif choice_func(best, val) == val:
                best = val

            if get_max:
                if alpha == None or (best != None and best > alpha):
                    alpha = best
            elif not get_max:
                if beta == None or (best != None and best < beta):
                    beta = best

            if alpha != None and beta != None and alpha > beta:
                break

        return best

    @staticmethod
    def tieChoice_random(node_list, get_max=True):
        node_list.sort(reverse=not get_max)
        best = []
        best_val = node_list[0]._value
        while len(node_list) > 0 and node_list[0]._value == best_val:
            best.append(node_list.pop())

        return random.choice(best)._item
