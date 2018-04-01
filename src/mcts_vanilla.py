import game, math
import random
import resource
import const
from resource import Move
import pickle
import datetime
from random import choice
from math import log, sqrt

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
        self.max_moves = 126  # 42 * 3 - Total pices on the board times half-plie 
        self.C = 1.4
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

        self.max_depth = 0
        legal = state.legalMovesList()

        if not legal:
            raise Exception('No legal moves')
        # If only one legal search about search
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(mv, state.update(mv)) for mv in legal]

        print (games, datetime.datetime.utcnow() - begin)

        percent_wins, move = max(
            [(self.wins.get(hash(S), 0) /
             self.plays.get(hash(S), 1),
             mv)
            for mv, S in moves_states], key= lambda b: b[0]
        )
        print(percent_wins, move)
        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get(hash(S), 0) /
              self.plays.get(hash(S), 1),
              self.wins.get(hash(S), 0),
              self.plays.get(hash(S), 0), mv)
             for mv, S in moves_states),
            reverse=True, key= lambda b: b[0]
        ):
            print ("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print ("Maximum depth searched:", self.max_depth)

        print('Exit MCTS')
        return move

    def run_simulation(self):
        plays, wins = self.plays, self.wins
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        visited_states = set()
        states_copy = self.state_history[:]
        current_state = states_copy[-1]
        player = current_state._player

        expand = True
        for t in range(self.max_moves):
            legal = current_state.legalMovesList()
            moves_states = [(mv, current_state.update(mv)) for mv in legal]

            if all(plays.get(hash(S)) for mv, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[hash(S)] for mv, S in moves_states))
                value, move, current_state = max(
                    [((wins[hash(S)] / plays[hash(S)]) +
                     self.C * sqrt(log_total / plays[hash(S)]), p, S)
                    for p, S in moves_states], key = lambda b: b[0]
                )

            else:
                # Otherwise, just make an arbitrary decision.
                move, current_state = choice(moves_states)


            states_copy.append(current_state)

            # Using the hash of the state since it is warranty to be unique
            if expand and hash(current_state) not in self.plays:
                expand = False
                self.plays[hash(current_state)] = 0
                self.wins[hash(current_state)] = 0
                if t > self.max_depth:
                    self.max_depth = t


            visited_states.add(current_state)

            player = current_state._player
            winner = self.checkWin(current_state)
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
