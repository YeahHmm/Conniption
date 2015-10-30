from copy import deepcopy, copy
from itertools import repeat, product, combinations
import os

from graph import Graph


class Move:
	action = ['flip', 'place', 'none']

	def __init__(self, action='none', player=-1, column=-1):
		self._action = action
		self._player = player
		self._column = column

	def toTupple(self):
		return (self._player, self._action, self._column)

	def __eq__(self, mv):
		return self.toTupple() == mv.toTupple()

	def __hash__(self):
		return self.toTupple().__hash__()

	def __repr__(self):
		return self.toTupple().__str__()


class SystemState:
	NUM_COLS = 7
	NUM_ROWS = 6
	LEN_SOL = 4

	MAX_FLIPS = 4

	SOLS_GRAPH = None

	def __init__(self, board=list(repeat([], 7)), prev_move=Move(), \
			cur_player=0, num_flips=(0, 0), is_down=0):
		self._board = board
		self._prev_move = prev_move
		self._cur_player = cur_player
		self._num_flips = num_flips
		self._is_down = is_down

	def update(self, mv):
		new_board = deepcopy(self._board)
		new_player = self._cur_player
		new_flips = deepcopy(self._num_flips)
		new_down = self._is_down

		if mv._action == 'flip':
			if self._prev_move._player == mv._player:
				new_player = int(not new_player)
			new_flips = tuple(map(lambda i: new_flips[i] + (i == self._cur_player), range(2)))
			new_down = int(not new_down)
		elif mv._action == 'place':
			if self._is_down:
				new_board[mv._column] = [self._cur_player] + new_board[mv._column]
			else:
				new_board[mv._column] = new_board[mv._column] + [self._cur_player]
		elif mv._action == 'none':
			if self._prev_move._player == mv._player:
				new_player = int(not new_player)

		return SystemState(new_board, mv, new_player, new_flips, new_down)

	def validMove(self, mv):
		if self._cur_player != mv._player:
			return False

		if mv._action == 'flip' or mv._action == 'none':
			if self._prev_move._action != 'flip':
				if self._prev_move._player != mv._player:
					return True
				elif self._prev_move._action != 'none':
					return True
		elif mv._action == 'place':
			if self._prev_move._action != mv._action:
				if self._prev_move._player == mv._player:
					if mv._column >= 0 and mv._column < SystemState.NUM_COLS:
						if len(self._board[mv._column]) < SystemState.NUM_ROWS:
							return True
		return False

	def isGoal(self, mv):
		row = len(self._board[mv._column])-1
		print (row)
		matrix = deepcopy(self.filledMatrix())
		col = copy(mv._column)
		print (col)
		# Horizontal
		i = col - 3 if col > 3 else 0
		while i <= col and i <= SystemState.NUM_COLS-4:
			if matrix[i][row]==matrix[i+1][row]==matrix[i+2][row]==matrix[i+3][row]:
				print('Horizontal' + str(matrix[row][i]) + ' ' + str(matrix[row][i+1]))
				return True
			i += 1
		# Vertical
		j = row - 3 if (row%7) > 3 else 0
		while j <= row and j <= SystemState.NUM_ROWS-4:
			if matrix[col][j]==matrix[col][j+1]==matrix[col][j+2]==matrix[col][j+3]:
				print('Vertical'+ str(matrix[col][j]) + ' ' + str(matrix[col][j+3]))
				return True
			j += 1
		# Diagonal Left to rigth down
		startCol = col - 3 if col > 3 else 0
		startRow = row + 3 if col > 3 else row + col
		while startCol <= col and startCol <= 3:
			if startRow > 2 and startRow <6:
				if matrix[startCol][startRow]==matrix[startCol+1][startRow-1]\
				==matrix[startCol+2][startRow-2]==matrix[startCol+3][startRow-3]:
					return True
			startCol += 1
			startRow -= 1
		# Diagonal left to Right up
		startCol = col - 3 if col > 3 else 0
		startRow = row - 3 if col > 3 else row - col
		while startCol <= col and startCol <= 3:
			if startRow >= 0 and startRow <4:
				if matrix[startCol][startRow]==matrix[startCol+1][startRow+1]\
				==matrix[startCol+2][startRow+2]==matrix[startCol+3][startRow+3]:
					return True
			startCol += 1
			startRow += 1

		return False
	def filledMatrix(self):
		if self._is_down:
			filled = list(map(lambda c: c[::-1] + [2]*(SystemState.NUM_ROWS - len(c)), self._board))
		else:
			filled = list(map(lambda c: c + [2]*(SystemState.NUM_ROWS - len(c)), self._board))
		return deepcopy(filled)

	def toTupple(self):
		boardTup = self.getBoardTuple()
		return (boardTup, self._prev_move, self._cur_player, self._num_flips, self._is_down)

	def getBoardTupple(self):
		return tuple(map(tuple, self._board))

	def __eq__(self, state):
		return (self.getBoardTupple(), self._is_down) == (mv.getBoardTupple(), mv._is_down)

	def __hash__(self):
		return (self.getBoardTupple(), self._is_down).__hash__()

	def __repr__(self):
		return self.toTupple().__repr__()

	def __str__(self):
		filled = self.filledMatrix()
		conv = lambda k: 'X' if k == 0 else 'O' if k == 1 else ' '
		filled = list(map(lambda c: list(map(conv, c)), filled))

		toPrint = ' ' + '----' * 14 + '\n|'
		for j in range(SystemState.NUM_ROWS - 1, -1, -1):
			for i in range(SystemState.NUM_COLS):
				toPrint += '{0:^7}|'.format(filled[i][j])

				if i % 7 == 6:
					toPrint += '\n'
					toPrint += ' ' + '----' * 14 + '\n|'
		toPrint = toPrint[:-1]

		toPrint += ' '
		for i in range(7):
			toPrint += '{0:^7} '.format(i+1)
		if self._cur_player == 0:
			toPrint += '\nPlayer 1:'
		else:
			toPrint += '\nPlayer 2:'

		return toPrint
	
	@staticmethod
	def _buildSols():
		ncols = SystemState.NUM_COLS
		nrows = SystemState.NUM_ROWS
		slen = SystemState.LEN_SOL

		graph = Graph()
		chain_dict = {}

		horiz_i = range(ncols - (slen - 1))
		horiz_j = range(nrows)
		horiz_start = product(horiz_i, horiz_j)
		for i, j in horiz_start:
			xlist = range(i, i + slen)
			chain = tuple((x, j) for x in xlist)
			graph.addVertex(chain)
		
		vert_i = range(ncols)
		vert_j = range(nrows - (slen - 1))
		vert_start = product(vert_i, vert_j)
		for i, j in vert_start:
			ylist = range(j, j + slen)
			chain = tuple((i, y) for y in ylist)
			graph.addVertex(chain)

		rdiag_i = range(ncols - (slen - 1))
		rdiag_j = range(nrows - (slen - 1))
		rdiag_start = product(rdiag_i, rdiag_j)
		for i, j in rdiag_start:
			xlist = range(i, i + slen)
			ylist = range(j, j + slen)
			chain = tuple((x, y) for x, y in zip(xlist, ylist))
			graph.addVertex(chain)

		ldiag_i = range(slen - 1, ncols)
		ldiag_j = range(nrows - (slen - 1))
		ldiag_start = product(ldiag_i, ldiag_j)
		for i, j in ldiag_start:
			xlist = range(i, i - slen - 1, -1)
			ylist = range(j, j + slen)
			chain = tuple((x, y) for x, y in zip(xlist, ylist))
			graph.addVertex(chain)

		for chain in graph.getVertices():
			keys = set()
			for i in range(1, slen - 1):
				keys.update(combinations(chain[1:], i))
				keys.update(combinations(chain[:3], i))
			for k in keys:
				if k not in chain_dict:
					chain_dict[k] = set()
				chain_dict[k].add(chain)

		for k in chain_dict:
			for chain in chain_dict[k]:
				for c in chain_dict[k]:
					if c is chain:
						continue
					graph.addEdge(chain, c, k)

		SystemState.SOLS_GRAPH = graph


SystemState._buildSols()
