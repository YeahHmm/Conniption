from copy import deepcopy
from itertools import repeat, chain
import os


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
	MAX_FLIPS = 4

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

	def isGoal(self):
		return False

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
		if self._is_down:
			filled = list(map(lambda c: c[::-1] + [2]*(SystemState.NUM_ROWS - len(c)), self._board))
		else:
			filled = list(map(lambda c: c + [2]*(SystemState.NUM_ROWS - len(c)), self._board))

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
