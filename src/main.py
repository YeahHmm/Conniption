import const

from resource import SystemState, Move
from game import Game, Human, AI
from evaluation import *

def place(game, player, col):
    game.update(Move('none', player))
    game.update(Move('place', player, col))
    game.update(Move('none', player))

def test():
    const.DEBUG = True
    ai1 = AI('ALEX', controlled_cells, 1, tieChoice=tieChoice_priority)
    ai2 = AI('ARMANDO', controlled_sols, 1, tieChoice=tieChoice_priority)
    player_pair = (ai1, ai2)
    game = Game(player_pair)

    place(game, 0, 3)
    place(game, 1, 3)
    place(game, 0, 3)
    place(game, 1, 3)
    place(game, 0, 2)
    place(game, 1, 2)
    place(game, 0, 2)
    #place(game, 1, 1)
    #print(cell_sol_hybrid(game.getState()))
    place(game, 1, 2)
    print(cell_sol_hybrid(game.getState()))
    #place(game, 0, 1)
    #print(cell_sol_hybrid(game.getState()))
    #place(game, 1, 3)
    #print(cell_sol_hybrid(game.getState()))
    #place(game, 0, 1)
    #print(cell_sol_hybrid(game.getState()))

    game.drawScreen()


def main():
    const.DEBUG = False
    const.MAX_FLIPS = 4

    #p1 = Human('ALEX')
    #p1 = AI('CELLS1', controlled_cells, 3, tieChoice=tieChoice_priority)
    #p1 = AI('SOLS1', controlled_sols, 3, tieChoice=tieChoice_priority)
    #p1 = AI('RANDOM1', random_move)
    p1 = AI('HYBRID1', cell_sol_hybrid, 3, tieChoice=tieChoice_priority)

    #p2 = Human('ALEX')
    p2 = AI('CELLS2', controlled_cells, 3, tieChoice=tieChoice_priority)
    #p2 = AI('SOLS2', controlled_sols, 3, tieChoice=tieChoice_priority)
    #p2 = AI('RANDOM2', random_move)
    #p2 = AI('HYBRID2', cell_sol_hybrid, 3, tieChoice=tieChoice_priority)
    player_pair = (p1, p2)
    game = Game(player_pair)

    count = 0
    while not game._gameEnd:
        game.drawScreen()
        mv = game.getCurPlayer().choose_move(game.getState())

        game.update(mv)
        game.checkWin()

    game.log("test.txt")
    if game._winner is None:
        msg = "The game was a draw!"
    else:
        msg = str(game._winner) + " wins!"
    game.drawScreen(msg)

if __name__ == "__main__":
    #test()
    main()
