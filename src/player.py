class Player:
    def __init__(self, name):
        self._name = name

    def toTuple(self):
        return (self._name,)

    def __eq__(self, other):
        return self.toTuple() == other.toTuple()

    def __hash__(self):
        return self.toTuple().__hash__()

    def __repr__(self):
        return self.toTuple().__repr__()

    def __str__(self):
        return str(self._name)

    def move(self, state):
        pass


class Human(Player):
    def move(self, state):
        print(state._cur_stage)

        if state._cur_stage == 0:
            pass
        elif state._cur_stage == 1:
            pass
        elif state._cur_stage == 2:
            pass
        return

class AI(Player):
    def __init__(self, name, eval_func):
        self.eval_func = eval_func
        super().__init__(name)

    def move(self, state):
        p_idx = state._player_pair.index(self)
        print(p_idx)
        return

    def toTuple(self):
        return (self._name, self.eval_func)
