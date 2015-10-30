import os

from printFunction import printboard
from resource import SystemState
from resource import Move

def main():
	cur_state = SystemState()

	winner = 2
	while True:
		os.system('clear')
		print (cur_state)
		val = input("input action (flip, place [1-7]): ").strip().split(' ')
		key = val[0]
		pos = -1
		if len(val) == 2:
			pos = int(val[1]) - 1
		move = Move(key, cur_state._cur_player, pos)
		if cur_state.validMove(move):
			cur_state = cur_state.update(move)
			isGoal, winner = cur_state._isGoal_flip()
			if isGoal:
				break
		else:
			print('Invalid move, try again')
			input('Press to continue')

	os.system('clear')
	print(cur_state)
	if winner == 0 or winner == 1:
		win_string = 'X' if winner == 0 else 'O' if winner == 1 else '-'
		print('Player %s wins!' % winner)
	else:
		print('Draw!')

if __name__ == "__main__":
	main()
