import os

from printFunction import printboard
from resource import SystemState
from resource import Move

def printState(state, prompt=''):
	os.system('clear')
	print (state)
	if prompt != '':
		print(prompt)


def main():
	cur_state = SystemState()
	valid = False
	prevMv = Move()
	is_goal = False
	winner = 2
	while not is_goal:
		for i in range (1,4):
			if i != 2:
				os.system('clear')
				printState (cur_state, "input action (flip/none): ")
				val = input().strip().split(' ')
				key = val[0]
				pos = -1
			else:
				os.system('clear')
				printState (cur_state, "input action (place [1-7]): ")
				val = input().strip().split(' ')
				key = 'place'
				pos = int(val[-1]) - 1
			move = Move(key, cur_state._cur_player, pos)
			prevMv = move
			valid = cur_state.validMove(move)
			if valid:
				cur_state = cur_state.update(move)
				is_goal, winner = cur_state.isGoal()
				if is_goal:
					break


	os.system('clear')
	print (cur_state)
	if winner == 0 or winner == 1:
		win_string = 'A' if winner == 0 else 'B' if winner == 1 else '-'
		print('Player %s wins!' %win_string)
	else:
		print('Draw!')


if __name__ == "__main__":
	main()
