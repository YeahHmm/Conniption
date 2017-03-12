import game


'''
Extends AI class (which is a child of the Player class) and allows for creation
of custom AI players.
Requires an evaluation function and supports choosing a depth limit and
a tie breaker between moves.
'''

class Qlearn(game.AI):

    def __init__(self, name, evalFunc, max_depth=1, tieChoice=None, \
        learning = False, epsilon=1.0, alpha=0.5):
        self.learning = learning
        self.alpha = alpha
        self.epsilon = epsilon
        self.Q = dict()

        '''
        Based on the game selection stages: (flip or none, place, flip or none)
        a different dict is provided. Place will indicate the column in
        which the coin will be placed while flip or none the decision to
        flip the board or not
        '''
        self.def_dic_flip = lambda: {
                                'place': 0.0,
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

    def choose_move(self, state):
        self.createQ(state)
        print (state._stage)
        print ('Number of states: ', len(self.Q))
        print (self.Q)
        moves = state.genMoves()
        mv = super().choose_move(state)
        print (mv, 'from Qlearn')
        return mv._item
