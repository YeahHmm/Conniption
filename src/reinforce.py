import game, math
import random
import resource
import const
from resource import Move
import pickle



'''
Extends player class and allows for creation a custom reinforcement agent
that uses Qlearn
Requires an evaluation function and supports choosing a depth limit and
a tie breaker between moves.
'''

class Qlearn(game.Player):

    def __init__(self, name, evalFunc, tieChoice=None, learning=False, epsilon=1.0, alpha=0.5, savedState=False):
        self.evalFunc = evalFunc
        self.learning = learning
        self.alpha = alpha
        self.epsilon = epsilon
        self.trial_num = 0
        if savedState:
            _file = './reinforcement_dict/' + const.GAME_NAME + '.pickle'
            self.Q = pickle.load(open(_file, 'rb'))
            self.epsilon = 0
            self.alpha = 0
        else:
            self.Q = dict()
        super().__init__(name)

        '''
        Based on the game selection stages: (flip or none, place, flip or none)
        a different dict is provided. Place will indicate the column in
        which the coin will be placed while flip or none the decision to
        flip the board or not
        '''
        self.def_dic_flip = lambda: {
                                'flip': 0.0,
                                'none': 0.0
        }
        self.def_dic_place = lambda: {
                                    0: 0.,
                                    1: 0.,
                                    2: 0.,
                                    3: 0.,
                                    4: 0.,
                                    5: 0.,
                                    6: 0.
        }

    def reset(self, testing=False):
        '''
        The reset function is called at the beginning of each trial.
        If 'testing' is true, it means the training trails have been
        completed and there is no need for more.
        '''
        self.trial_num += 1
        a = 0.004
        self.epsilon = math.exp(1)**(-a*self.trial_num)
        #self.epsilon = self.epsilon - 0.010
        if testing == True:
            self.epsilon = 0
            self.alpha = 0
        return None


    def createQ(self, state):
        '''
        Create dict based on the system state and the stage in which the
        system is located. The state is find by the hash function generated
        from the board tuples.

        The hash representation contains the board and the stage.
        More variables could be added in the feature, this two were
        selected in order to keep the number of instances as small
        as possible.
        '''
        if self.learning and state.__hash__() not in self.Q:
            if state._stage == 0 or state._stage == 2:
                self.Q[state.__hash__()] = self.def_dic_flip()
            else:
                self.Q[state.__hash__()] = self.def_dic_place()


    def get_maxQ(self, state):
        '''
        Returns Q-value list based on the player that is requested,
        player one it returns the biggest positive number,
        while player two returns the smallest negative number.
        This is due to player one maximizing while player two
        minimizing
        '''
        items = self.Q[state.__hash__()].values()
        maxQ = sorted(items, reverse= state._player == 0)
        return maxQ

    def choose_action(self, state):
        '''
        Generate all valid actions from the genMoves
        algorithm. Then build the moves Dictionary
        depending on the element being built.
        '''
        valid_moves = list(state.genMoves())
        # If stage one or three, get the action
        if state._stage == 0 or state._stage == 2:
            moves = [x._action for x in valid_moves]
        # Else get the column to be placed
        else:
            valid_moves = sorted(valid_moves, key= lambda x: x._column)
            moves = [x._column for x in valid_moves]
        rand_num = random.randint(0, len(moves)-1)

        # If no more flips are allowed, select none.
        # If previous move was not a flip
        # No consecutive flips allowed
        if len(moves) > 1:
            if self.epsilon > random.random():
                # return a rand move with epsilon probability
                action = moves[rand_num]
            else:
                # Get sorted list of states
                # Make sure the element select from Qlist
                # is a valid element.
                # If it is bestQ, but not valid (due to not being a possible
                # move) check the next best Q value
                max_states = []
                maxQList = self.get_maxQ(state)
                for maxQ in maxQList:
                    for key in moves:
                        if maxQ == self.Q[state.__hash__()][key]:
                            max_states.append(key)
                    if max_states:
                        action = random.choice(max_states)
                        return action
        else:
            action = moves[0]

        return action


    def learn(self, state, move, action):
        if self.learning:
            new_state = state.update(move)
            reward = self.evalFunc(new_state)
            # Add a bias against flipping
            if action == 'none':
                if state._player == 0:
                    if reward > 0:
                        reward *= 1.5
                    else:
                        reward /= 1.5
                else:
                    if reward < 0:
                        reward *= 1.5
                    else:
                        reward /= 1.5


            if state.__hash__() not in self.Q:
                self.createQ(state)
            rate = self.alpha
            #print (self.Q[state.__hash__()])
            old_q = self.Q[state.__hash__()][action]
            #new_q = old_q + (rate * ((reward)- old_q))
            new_q = (1 - rate) * old_q + (reward * self.alpha)
            self.Q[state.__hash__()][action] = new_q


        return

    def choose_move(self, state):
        self.createQ(state)
        _action = self.choose_action(state)
        if state._stage == 0 or state._stage == 2:
            mv = Move(_action, state._player)
        else:
            mv = Move('place', state._player, _action)

        self.learn(state, mv, _action)
        #print (mv, 'from Qlearn')
        return mv


'''
Extends AI class (which is a child of the Player class) and allows for creation
of custom AI players.
Requires an evaluation function and supports choosing a depth limit and
a tie breaker between moves.
'''

class MinimaxQlearn(game.AI):

    def __init__(self, name, evalFunc, max_depth=1, tieChoice=None, \
        learning = False, epsilon=1.0, alpha=0.5, savedState=False):
        self.learning = learning
        self.alpha = alpha
        self.epsilon = epsilon
        self.trial_num = 0
        if savedState:
            _file = './reinforcement_dict/' + const.GAME_NAME + '.pickle'
            self.Q = pickle.load(open(_file, 'rb'))
            self.epsilon = 0
            self.alpha = 0
        else:
            self.Q = dict()


        '''
        Based on the game selection stages: (flip or none, place, flip or none)
        a different dict is provided. Place will indicate the column in
        which the coin will be placed while flip or none the decision to
        flip the board or not
        '''
        self.def_dic_flip = lambda: {
                                'flip': 0.0,
                                'none': 0.0
        }
        self.def_dic_place = lambda: {
                                    0: 0.,
                                    1: 0.,
                                    2: 0.,
                                    3: 0.,
                                    4: 0.,
                                    5: 0.,
                                    6: 0.
        }
        super().__init__(name, evalFunc, max_depth=max_depth, \
                tieChoice=tieChoice)

    '''
    The reset function is called at the beginning of each trial.
    If 'testing' is true, it means the training trails have been
    completed and there is no need for more.
    '''
    def reset(self, testing=False):
        self.trial_num += 1
        a = 0.005
        #self.epsilon = abs(math.cos( a * self.trial_num))
        #self.epsilon = self.epsilon - 0.0005
        self.epsilon = math.exp(1)**(-a*self.trial_num)
        if testing == True:
            self.epsilon = 0
            self.alpha = 0
        return None


    '''
    Create dict based on the system state and the stage in which the
    system is located. The state is find by the hash function generated
    from the board tuples.

    The hash representation contains the board and the stage.
    More variables could be added in the feature, this two were
    selected in order to keep the number of instances as small
    as possible.
    '''
    def createQ(self, state):
        if self.learning and state.__hash__() not in self.Q:
            if state._stage == 0 or state._stage == 2:
                self.Q[state.__hash__()] = self.def_dic_flip()
            else:
                self.Q[state.__hash__()] = self.def_dic_place()


    '''
    Returns Q-value based on the player that is requested,
    player one it returns the biggest positive number,
    while player two returns the smallest negative number.
    This is due to player one maximizing while player two
    minimizing
    '''
    def get_maxQ(self, state):
        items = self.Q[state.__hash__()].values()
        maxQ = sorted(items, reverse= state._player == 0)
        return maxQ


    def choose_action(self, state):
        '''
        Generate all valid actions from the genMoves
        algorithm. Then build the moves Dictionary
        depending on the element being built.
        '''
        valid_moves = list(state.genMoves())
        if state._stage == 0 or state._stage == 2:
            moves = [x._action for x in valid_moves]
        else:
            valid_moves = sorted(valid_moves, key= lambda x: x._column)
            moves = [x._column for x in valid_moves]
        rand_num = random.randint(0, len(moves)-1)
        #print ('Moves:', moves, 'r', rand_num)


        # If no more flips are allowed, select none.
        # If previous move was not a flip
        # No consecutive flips allowed
        if len(moves) > 1:
            if self.epsilon > random.random():
                # return a rand move with epsilon probability
                action = moves[rand_num]
            else:
                # Get sorted list of bestQ values.
                # Make sure the element select from Qlist
                # is a valid element.
                # If it is bestQ, but not valid max_states list will be empty
                # (due to not being a possible move) check the next best Q value
                max_states = []
                maxQList = self.get_maxQ(state)
                for maxQ in maxQList:
                    for key in moves:
                        if maxQ == self.Q[state.__hash__()][key]:
                            max_states.append(key)
                    if max_states:
                        action = random.choice(max_states)
                        return action
        else:
            action = moves[0]

        return action

    def learn(self, state, move, action):
        if self.learning:
            moves = super().choose_move(state)
            #print ('Selected mov: ', move)
            reward = [x._value for x in moves if x._item == move]
            reward = reward[0]
            #print ('reward: ', reward)

            if state.__hash__() not in self.Q:
                self.createQ(state)
            rate = self.alpha
            old_q = self.Q[state.__hash__()][action]
            #new_q = old_q + (rate * ((reward)- old_q))
            new_q = (1 - rate) * old_q + (reward * self.alpha)
            self.Q[state.__hash__()][action] = new_q

        return

    def choose_move(self, state):
        self.createQ(state)
        _action = self.choose_action(state)
        if state._stage == 0 or state._stage == 2:
            mv = Move(_action, state._player)
        else:
            mv = Move('place', state._player, _action)

        self.learn(state, mv, _action)
        return mv
