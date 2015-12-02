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


'''
Class used by main game loop to handle printing, logging, players,
and other functions with SystemState as a backend.
'''
class Game:
    def __init__(self, player_pair):
        self._state = SystemState()
        self._player_pair = player_pair
        self._history = []
        self._winner = None
        self._gameEnd = False

    def getState(self):
        return self._state

    '''
    Get Player object from SystemState _player value
    '''
    def getCurPlayer(self):
        return self._player_pair[self._state._player]

    '''
    Update SystemState and record Move
    '''
    def update(self, mv):
        self._state = self._state.update(mv)
        self._history.append(mv)

    '''
    Check and return whether game is complete and record winning Player
    '''
    def checkWin(self):
        self._gameEnd, winner = self._state.isGoal()
        if self._gameEnd and winner != const.EMPTY_VAL:
            self._winner = self._player_pair[winner]

        return self._gameEnd

    '''
    Save game information with pickle
    '''
    def save(self, fname):
        pair = self._player_pair
        if os.path.isfile(fname):
            data = pickle.load(open(fname, 'rb'))
        else:
            data = []

        players = tuple(map(lambda p: p._name if p is not None else p, pair))
        win_name = self._winner._name if self._winner is not None else None
        win_state = (self._gameEnd, win_name)
        mv_list = tuple(self._history)

        game = (players, win_state, mv_list)
        data.append(game)

        f = open(fname, 'wb')
        pickle.dump(data, f)
        f.close()

    '''
    Write game information to text file
    '''
    def log(self, fname):
        pair = self._player_pair
        f = open(fname, 'a')

        line = ''
        line += str((pair[0]._name, pair[1]._name))
        line += ',' + str((self._gameEnd, self._winner._name))
        line += ',' + str(self._history)

        f.write(line + "\n")
        f.close()

    '''
    Draw game screen with optional message. Clears previous screen unless
    const.DEBUG denotes debug mode.
    '''
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


'''
Base Player class intended for extension.
'''
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


'''
Extends Player class and implements a choose_move() function that allows
manual play.
'''
class Human(Player):
    '''
    Asks the user to choose a move. Returns a Move object after a valid Move
    is chosen.
    '''
    def choose_move(self, state):
        mv = None
        # Do not return until Move is valid
        while not mv or not state.validMove(mv):
            if state._stage == 0 or state._stage == 2:
                # Prompt for pass or flip if both are options
                if state._prev_move._action != 'flip' and \
                        state._num_flips[state._player] < const.MAX_FLIPS:
                    msg = 'Flip or Pass [f or p]:'
                    mapping = {'f':'flip', 'p':'none'}
                # Automatically pass if only option is a none Move
                else:
                    mv = Move('none', state._player)
                    break
            # Prompt for column if in 2nd stage of turn
            elif state._stage == 1:
                msg = 'Place [1-%d]:' % (const.NUM_COLS)
                mapping = {str(n) : 'place' for n in range(1, const.NUM_COLS + 1)}

            # Get key pressed by user and create a corresponding Move object
            sys.stdout.flush()
            key = prompt(msg).lower()
            if key in mapping:
                if key.isnumeric():
                    mv = Move(mapping[key], state._player, int(key)-1)
                else:
                    mv = Move(mapping[key], state._player)

        return mv


'''
Extends Player class and allows for creation of custom AI players. Requires
an evaluation function and supports choosing a depth limit and a tie breaker
between moves.
'''
class AI(Player):
    def __init__(self, name, evalFunc, max_depth=1, tieChoice=None):
        self.evalFunc = evalFunc
        self.tieChoice = tieChoice
        self._max_depth = max_depth
        super().__init__(name)

    '''
    Run a minimax search to choose a Move
    '''
    def choose_move(self, state):
        mv = self._minimax(state, state._player == 0)
        return mv

    def toTuple(self):
        return (self._name, self.evalFunc)

    '''
    Base minimax function. Initializes a recursive search with alpha-beta
    pruning.
    '''
    def _minimax(self, base_state, get_max):
        mv_list = base_state.genMoves()

        # Data for next recursion
        cmod = base_state._stage == const.NUM_STAGES - 1
        new_choice = cmod ^ get_max
        new_depth = new_choice != get_max

        # Get list of Nodes with Move objects as items and evaluation
        # scores as values
        children = []
        for mv in mv_list:
            new_state = base_state.update(mv)
            tup = new_state.getBoardTuple()
            mv_val = self._minimax_help(new_state, new_depth, \
                    new_choice, get_max)

            children.append(Node(mv_val, mv))

        # Sort the options and choose the best using the provided tie breaker
        # if one was provided. Otherwise use the built-in choice function.
        if self.tieChoice is not None:
            return self.tieChoice(children, get_max)
        else:
            return AI.tieChoice_random(children, get_max)

    def _minimax_help(self, base_state, depth, get_max, init_choice,
            alpha=None, beta=None):
        # Run evaluation function at depth limit
        if depth > self._max_depth and base_state._stage == 0:
            val = self.evalFunc(base_state)
            return val

        # Run evaluation function if end of game found
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
            # Get next state and recurse
            new_state = base_state.update(mv)
            val = self._minimax_help(new_state, new_depth, \
                    new_choice, init_choice, alpha, beta)

            # Update best if no best found or if val is preferable
            if best == None:
                best = val
            elif choice_func(best, val) == val:
                best = val

            # Update alpha if maximizing and best is larger
            if get_max:
                if alpha == None or (best != None and best > alpha):
                    alpha = best
            # Update beta if minimizing and best is smaller
            elif not get_max:
                if beta == None or (best != None and best < beta):
                    beta = best

            # Stop when alpha is larger than beta (prune)
            if alpha != None and beta != None and alpha > beta:
                break

        # Return best evaluation value
        return best

    '''
    A default tie breaker where ties are broken at random
    '''
    @staticmethod
    def tieChoice_random(node_list, get_max=True):
        # Sort based upon minimizing or maximizing
        node_list.sort(reverse=not get_max)

        # Grab the best values
        best = []
        best_val = node_list[0]._value
        while len(node_list) > 0 and node_list[0]._value == best_val:
            best.append(node_list.pop())

        # Choose a random one from the list
        return random.choice(best)._item
