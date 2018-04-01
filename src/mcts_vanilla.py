import game, math
import random
import resource
import const
from resource import Move
import pickle
import datetime
from random import choice

'''
    Tutorial obtained from:
    https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
'''

'''
Extends player class and allows for creation a custom MonteCarlo Tree Search
AI.

Ideally, this AI will compete against the minimax agents. We will test how
well it does.
'''

class MCTS_AI(game.Player):

    def __init__(self, name, seconds=30):
        super().__init__(name)
        self.state_history = []
        self.game = game
        self.gameState = None
        self.max_moves = 100
        seconds = 30
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.wins = {}
        self.plays = {}



    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.state_history.append(state)

    # Replaces get_play()
    def choose_move(self, state):
        '''
        This one is part of the AI player that I have in my own implementation.
        Should return a move that the player is taking
        '''
        self.update(state)
        begin = datetime.datetime.utcnow()
        #while datetime.datetime.utcnow() - begin < self.calculation_time:
        self.run_simulation()
        print('Exit MCTS')

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        visited_states = set()
        states_copy = self.state_history[:]
        current_state = states_copy[-1]
        player = current_state._player

        expand = True
        for t in range(self.max_moves):
            legal = current_state.legalMovesList()
            print ("Legal Moves: {}".format(str(legal)))
            mv = choice(legal)
            print ("Choice: {}".format(str(mv)))
            print(current_state)
            current_state = current_state.update(mv)
            states_copy.append(current_state)

            # Using the hash of the state since it is warranty to be unique
            if expand and hash(current_state) not in self.plays:
                expand = False
                self.plays[hash(current_state)] = 0
                self.wins[hash(current_state)] = 0


            visited_states.add(current_state)

            player = current_state._player
            winner = self.checkWin(current_state)
            print('Winner is: ' + str(winner))
            if winner:
                break

        for state in visited_states:
            if hash(state) not in self.plays:
                continue
            self.plays[hash(state)] +=1
            if player == winner:
                self.wins[hash(state)] += 1

    # return the winner if the game ended, else None
    def checkWin(self, state):
        gameEnd, winner = state.isGoal()
        return winner if gameEnd else None
