from copy import deepcopy
from itertools import repeat, chain
import os


class Move:
	action = {'flip':'flip', 'place':'place', 'none':'none'}

	def __init__(self, act_key='none', player=0, column=-1):
		self._action = Move.action[act_key]
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
			cur_player=1, num_flips=(0, 0), is_down=0):
		self._board = board
		self._prev_move = prev_move
		self._cur_player = cur_player
		self._num_flips = num_flips
		self._is_down = is_down

	def update(self, mv):
		new_board = deepcopy(self._board)
		new_player = self._cur_player * -1
		new_flips = deepcopy(self._num_flips)
		new_down = self._is_down

		if mv._action == Move.action['flip']:
			new_flips = tuple(map(lambda i: new_flips[i] + (i == self._cur_player), range(2)))
			new_down = not new_down
		elif mv._action == Move.action['place']:
			if self._is_down:
				new_board[mv._column] += [self._cur_player]
			else:
				new_board[mv._column] =  new_board[mv._column] + [self._cur_player]

		return SystemState(new_board, mv, new_player, new_flips, new_down)

	def validMove(self, mv):
		if mv._player != self._cur_player:
			return False

		if mv._action == Move.action['flip']:
			if self._prev_move._action == Move.action['flip']:
				return False
			elif self._num_flips[self._cur_player] >= SystemState.MAX_FLIPS:
				return False
			else:
				return True
		elif mv._action == Move.action['place']:
			print("TEST")
			if len(self._board[mv._column]) >= SystemState.NUM_ROWS:
				return False
			else:
				return True

		return False

	def isGoal(self):
		return False

	def toTupple(self):
		boardTup = tuple(map(tuple, self._board))
		return (boardTup, self._prev_move, self._cur_player, self._num_flips, self._is_down)

	def __eq__(self, state):
		return self.toTupple() == state.toTupple()

	def __hash__(self):
		return self.toTupple().__hash__()

	def __repr__(self):
		return self.toTupple().__repr__()

	def __str__(self):
		if self._is_down:
			filled = list(map(lambda c: c[::-1] + [0]*(SystemState.NUM_ROWS - len(c)), self._board))
		else:
			filled = list(map(lambda c: c + [0]*(SystemState.NUM_ROWS - len(c)), self._board))
		filled = list(map(lambda c: list(map(lambda k: 'X' if k == 1 else 'O' if k == -1 else ' ', c)), filled))

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

		return toPrint
