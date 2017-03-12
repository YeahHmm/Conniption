import game


'''
Extends AI class (which is a child of the Player class) and allows for creation
of custom AI players. 
Requires an evaluation function and supports choosing a depth limit and
a tie breaker between moves.
'''

class Qlearn(game.AI):

    def __init__(self, name, evalFunc, max_depth=1, tieChoice=None):
        super().__init__(name, evalFunc, max_depth=max_depth, \
                tieChoice=tieChoice)

    def choose_move(self, state):
        return super().choose_move(state)
