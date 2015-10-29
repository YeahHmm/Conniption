#   _data = {
#	   vertex0 : {edge0_1 : {vertex1}, edge0_2 : {vertex2}, ...},
#	   vertex1 : {edge1_02 : {vertex0, vertex2}, ...},
#	   vertex2 : {edge2_1 : {vertex1}, ...},
#	   ...
#   }

from copy import deepcopy
from itertools import chain


class Graph:
	def __init__(self):
		self._vset = set()
		self._data = {}

	# == ACCESSORS ==
	def isEmpty(self):
		return len(self._vset) == 0

	def hasVertex(self, v):
		return v in self._vset

	def hasEdge(self, v1, v2):
		if v1 in self._vset:
			for e in self._data[v1]:
				if v2 in self._data[v1][e]:
					return True
			return False
		return False

	def getEdges(self, v1, v2):
		if v1 in self._vset:
			return {l for l in filter(lambda k: v2 in self._data[v1][k], self._data[v1])}

	def neighbors(self, v, e=None):
		if v in self._vset:
			if e is None:
				return set(chain(*self._data[v].values()))
			elif e in self._data[v]:
				return deepcopy(self._data[v][e])
			else:
				return set()

	# == MUTATORS ==
	def addVertex(self, v):
		self._vset.add(v)
		self._data[v] = {}

	def removeVertex(self, v):
		if v in self._vset:
			for v_i in self._data:
				if self.hasEdge(v_i, v):
					self.removeEdge(v_i, v)
			self._vset.remove(v)
			del self._data[v]

	def addEdge(self, v1, v2, e):
		if v1 and v2 in self._vset:
			if e not in self._data[v1]:
				self._data[v1][e] = set()
			self._data[v1][e].add(v2)

	def removeEdge(self, v1, v2):
		if v1 and v2 in self._vset:
			for e in self._data[v1]:
				if v2 in self._data[v1][e]:
					self._data[v1][e].remove(v2)

'''
def buildTest():
	g = Digraph()
	a = (0, 1, 2, 3)
	b = (1, 2, 3, 4)
	c = (2, 3, 4, 5)
	
	g.addVertex(a)
	g.addVertex(b)
	g.addVertex(c)

	g.addEdge(a, b, (1,))
	g.addEdge(a, b, (2,))
	g.addEdge(a, b, (3,))
	g.addEdge(a, b, (1, 2,))
	g.addEdge(a, b, (1, 3,))
	g.addEdge(a, b, (2, 3,))
	g.addEdge(b, a, (1,))
	g.addEdge(b, a, (2,))
	g.addEdge(b, a, (3,))
	g.addEdge(b, a, (1, 2,))
	g.addEdge(b, a, (1, 3,))
	g.addEdge(b, a, (2, 3,))

	g.addEdge(a, c, (2,))
	g.addEdge(a, c, (3,))
	g.addEdge(a, c, (2, 3,))
	g.addEdge(c, a, (2,))
	g.addEdge(c, a, (3,))
	g.addEdge(c, a, (2, 3,))

	g.addEdge(b, c, (2,))
	g.addEdge(b, c, (3,))
	g.addEdge(b, c, (4,))
	g.addEdge(b, c, (2, 3,))
	g.addEdge(b, c, (2, 4,))
	g.addEdge(b, c, (3, 4,))
	g.addEdge(c, b, (2,))
	g.addEdge(c, b, (3,))
	g.addEdge(c, b, (4,))
	g.addEdge(c, b, (2, 3,))
	g.addEdge(c, b, (2, 4,))
	g.addEdge(c, b, (3, 4,))

	return g
'''
