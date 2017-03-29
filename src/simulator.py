import os
import time
import const
import pickle

'''
Simulator class that manage the needed loop to make a
Qlearn agent to train as long as the epsilon decay
is bigger than the tolerance
'''
class Simulator(object):

    # Set up environment variables
    const.MAX_FLIPS = 4
    const.NUM_LOOK = 3

    def __init__(self, game,debug=False):
        self._game = game
        const.DEBUG = debug
        # stats dict records the w/l of each player
        self.stats = {}
        self.stats['results'] = [0,0,0]


    def run(self, tolerance=0.05, n_test=0):
        """
        Run a simulation of the environment.

        'tolerance' is the minimum epsilon necessary to begin testing (if enabled)
        'n_test' is the number of testing trials simulated

        Note that the minimum number of training trials is always 20.
        """
        a =  self.getQlearnAgent(self._game)
        total_trials = 1
        testing = False
        trial = 1

        while True:
            # flip testing when more than 20 trials and
            # epsilon less than tolerance
            if not testing:
                if total_trials > 20:
                    if a.learning:
                        if a.epsilon < tolerance:
                        #if total_trials > 3000:
                            testing = True
                            trial = 1
                            self.stats['results'] = [0,0,0]
                    else:
                        testing = True
                        trial = 1
            else:
                if trial > n_test:
                    break
            while not self._game.checkWin():
                if testing:
                    self._game.drawScreen()
                mv = self._game.getCurPlayer().choose_move(self._game.getState())
                self._game.update(mv)
            # Prompt for replay
            if self._game._winner is None:
                msg = "The game was a draw!"
                self.stats['results'][2] += 1
            else:
                msg = str(self._game._winner) + " wins!"
                self.stats['results'][self._game._player_pair.index(self._game._winner)] += 1
            print (msg)
            self._game.drawScreen()
            self._game.reset(testing=testing)
            #a.reset(testing=testing)

            print ("/-------------------------")
            if testing:
                print ("| Testing trial {}".format(trial))
                print ('Epsilon: ', a.epsilon)
            else:
                print ("| Training trial {}".format(trial))
                print ('Epsilon: ', a.epsilon)

            print ("\-------------------------")
            self.printResults()


            total_trials = total_trials + 1
            trial = trial + 1
        print (len(a.Q))
        print ('Training size: ', total_trials - trial)
        self.saveGeneratedDict(a)


    def getQlearnAgent(self, game):
        '''
        Returns the agent that has a QLEARN agent declared
        Exits the simulation in the case none of them is
        declared as such
        '''
        if game._player_pair[0]._name == 'QLEARN1':
            a = game._player_pair[0]
            return a
        elif game._player_pair[1]._name == 'QLEARN2':
            a = game._player_pair[1]
            return a
        elif game._player_pair[0]._name == 'MINIMAXQ1':
            a = game._player_pair[0]
            return a
        elif game._player_pair[1]._name == 'MINIMAXQ2':
            a = game._player_pair[1]
            return a
        else:
            print('One of the player agents need to be Qlearn')
            os.sys.exit()

    def printResults(self):
        '''
        Print the results out of the game from the stats class
        '''
        p1 = self._game._player_pair[0]
        p2 = self._game._player_pair[1]
        results = self.stats['results']
        '''
        if results[0] > results[2]:
            msg = str(p1)
        elif results[0] < results[2]:
            msg = str(p2)
        else:
            msg = 'It was a tie'
        '''
        msg = ''
        msg = '\n' + msg + '\n'
        msg += str(p1) + ': ' + '/'.join(map(str, results))
        msg += '\n'
        msg += str(p2) + ': ' + '/'.join(map(str, (results[1], results[0], results[2])))
        msg += '\n'
        print(msg)

    def saveGeneratedDict(self, player):
        '''
        Save dictionary object generated during the training in order
        to be able to use the player without training it again.
        '''
        save_dir = './reinforcement_dict/' + self.getGameNames() + '.pickle'
        with open(save_dir, 'wb') as handle:
            pickle.dump(player.Q, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def getGameNames(self):
        '''
        Return game names, for both payer one and player two
        '''
        p1 = self.game._player_pair[0]._name
        p2 = self.game._player_pair[1]._name
        return p1+p2
