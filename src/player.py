class Player:
    def __init__(self,name,turn=0):
        self._name = name

    def toTuple(self):
        return (self._name)

    def __eq__(self, other):
        return self.toTuple() == other.toTuple()

    def __hash__(self):
        return self.toTuple().__hash__()

    def __repr__(self):
        return self.toTuple().__repr__()

    def __str__(self):
        return self._name

    def move(self, state):
        pass

