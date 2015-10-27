from itertools import repeat

class SystemState:
    def __init__(self):
        self._board = list(repeat(list(repeat(0, 6)), 7))
        self._prev_move = None
        self._cur_player = 0
        self._num_flips = (0, 0)
        self._is_up = 0
    
    def update(self, mv):
        return

    def validMove(self, mv):
        return False

    def isGoal(self):
        return False

    def toTupple(self):
        boardTup = tuple(map(tuple, self._board))
        return (boardTup, self._prev_move, self._cur_player, self._num_flips, self._is_up)

    def __eq__(self, state):
        return self.toTupple() == state.toTupple()

    def __hash__(self):
        return self.toTupple().__hash__()


class Move:
    action = ['flip', 'place', 'none']
    
    def __init__(self):
        self._player = 0
        self._key = 'none'
        self._column = -1

    def toTupple(self):
        return (self._player, self._key, self._column)

    def __eq__(self, mv):
        return self.toTupple() == mv.toTupple()

    def __hash__(self):
        return self.toTupple().__hash__()
