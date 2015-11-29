import const
import csv
#import sys
#sys.setrecursionlimit(10000)

from evaluation import *
from game import Game, Human, AI
from printing import prompt
from resource import SystemState, Move

def place(game, player, col):
	game.update(Move('none', player))
	game.update(Move('place', player, col))
	game.update(Move('none', player))

def test():
	const.DEBUG = True
	ai1 = AI('HYBRID1', cell_sol_hybrid, 3, tieChoice=tieChoice_priority)
	ai2 = Human('ALEX')
	player_pair = (ai1, ai2)
	game = Game(player_pair)

	f = open('tst.log')
	lf = [l.strip() for l in lf]
	last = lf[-1]
	seq = last.split(',')


	game.drawScreen()

def printStatsToFile():

	with open("results.csv", 'w') as csvf:
		write = csv.writer(csvf)
		write.writerow(['Evaluation', 'Hy-wins','Hy-Draws', 'Hy-totalGames', 'Hy-AvgMoves',\
						'Cells-wins','Cells-Draws', 'Cells-totalGames', 'Cells-AvgMoves', \
						'Solution-wins','Solution-Draws', 'Solution-totalGames', 'Solution-AvgMoves'])
		for x in range(4):

			write.writerow(['1', '2', '3', '4'])


def promptContinue(stats):
	p1 = stats['game']._player_pair[0]
	p2 = stats['game']._player_pair[1]
	results = stats['results']
	msg = str(p1) + ': ' + '/'.join(map(str, results))
	msg += '\n'
	msg += str(p2) + ': ' + '/'.join(map(str, (results[1], results[0], results[2])))
	msg += '\n'
	msg += "Play again [y/N]?"

	response = None
	while response == None:
		stats['game'].drawScreen()
		key = prompt(msg).lower()
		response = True if key == 'y' else False if key =='n' else None

	return response

def main():
	const.DEBUG = False
	const.MAX_FLIPS = 4

	ptype = [None, None]
	ptype[0] = input("Enter Player 1 type: ").upper()
	ptype[1] = input("Enter Player 2 type: ").upper()

	pname = [ptype[0]+'1', ptype[1]+'2']
	pclass = [AI, AI]
	pfunc = [None, None]
	for i in range(2):
		if ptype[i] == "RANDOM":
			pfunc[i] = random_move
		elif ptype[i] == "CELLS":
			pfunc[i] = controlled_cells
		elif ptype[i] == "SOLS":
			pfunc[i] = controlled_sols
		elif ptype[i] == "HYBRID":
			pfunc[i] = cell_sol_hybrid
		elif ptype[i] == "HUMAN":
			pclass[i] = Human
			pname[i] = input("Enter Player %d name: " % (i+1))

	if pclass[0] == Human:
		p1 = pclass[0](pname[0])
	else:
		p1 = pclass[0](pname[0], pfunc[0], 3, tieChoice=tieChoice_priority)

	if pclass[1] == Human:
		p2 = pclass[1](pname[1])
	else:
		p2 = pclass[1](pname[1], pfunc[1], 3, tieChoice=tieChoice_priority)

	#p1 = Human('ALEX')
	#p1 = AI('CELLS1', controlled_cells, 3, tieChoice=tieChoice_priority)
	#p1 = AI('SOLS1', controlled_sols, 3, tieChoice=tieChoice_priority)
	#p1 = AI('RANDOM1', random_move)
	#p1 = AI('HYBRID1', cell_sol_hybrid, 3, tieChoice=tieChoice_priority)

	#p2 = Human('ALEX')
	#p2 = AI('CELLS2', controlled_cells, 3, tieChoice=tieChoice_priority)
	#p2 = AI('SOLS2', controlled_sols, 3, tieChoice=tieChoice_priority)
	#p2 = AI('RANDOM2', random_move)
	#p2 = AI('HYBRID2', cell_sol_hybrid, 3, tieChoice=tieChoice_priority)
	player_pair = (p1, p2)
	play_again = True

	stats = {}
	stats['results'] = [0, 0, 0]

	while play_again:
		game = Game(player_pair)
		stats['game'] = game

		while not game._gameEnd:
			game.drawScreen()
			mv = game.getCurPlayer().choose_move(game.getState())

			game.update(mv)
			game.checkWin()
			game.log('tst.log')

		game.log("test.txt")
		if game._winner is None:
			msg = "The game was a draw!"
			stats['results'][2] += 1
		else:
			msg = str(game._winner) + " wins!"
			stats['results'][game._player_pair.index(game._winner)] += 1
		game.drawScreen(msg)

		play_again = promptContinue(stats)


if __name__ == "__main__":
	#test()
	printStatsToFile()
	main()
