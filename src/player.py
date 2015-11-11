class Player:
    def __init__(self,name,turn=0):
        self._name = name
        self._turn = turn
        self._flips = 4

    def toTuple(self):
        return (self._name, self._turn, self._flips)

    def __eq__(self, other):
        return self.toTuple() == other.toTuple()

    def __hash__(self):
        return self.toTuple().__hash__()

    def __repr__(self):
        return self.toTuple().__str__()

    def move():
        pass
