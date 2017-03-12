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
        self.def_dic = lambda: {
                                'place': {-1: 0.},
                                'flip': {
                                        0: 0.,
                                        1: 0.,
                                        2: 0.,
                                        3: 0.,
                                        4: 0.,
                                        5: 0.,
                                        6: 0.
                                },
                                'none': {-1: 0.}
        }
        super().__init__(name, evalFunc, max_depth=max_depth, \
                tieChoice=tieChoice)


    def createQ(self):
        pass

    def choose_move(self, state):
        mv = super().choose_move(state)
        print (mv, 'from Qlearn')
        return mv._item
