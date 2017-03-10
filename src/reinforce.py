import game



class Qlearn(game.AI):

    def __init__(self, name, evalFunc, max_depth=1, tieChoice=None):
        super().__init__(name, evalFunc, max_depth=max_depth, \
                tieChoice=tieChoice)

    def choose_move(self, state):
        return super.choose_move(state)
