from itertools import repeat

class SystemState:
    def __init__(self):
        self._board = list(repeat(list(repeat(0, 6)), 7))
        self._prev_move = None
        self._cur_player = 0
        self._num_flips
    
    def update(self, mv):
        return

    def validMove(self, mv):
        return False

    def isGoal(self):
        return False


class Move:
    action = ['flip', 'place', 'none']
    
    def __init__(self):
        self._player = 0
        self._key = 'none'
        self._column = -1
