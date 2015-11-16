import const

from printing import printState
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


def main2():
    const.DEBUG = True
    #p1 = Human('ALEX')
    p1 = AI('CELLS1', controlled_cells, 3, tieChoice=tieChoice_priority)
    #p1 = AI('SOLS1', controlled_sols, 5, tieChoice=tieChoice_priority)
    #p1 = AI('RANDOM1', random_move)
    #p1 = AI('HYBRID1', cell_sol_hybrid, 3, tieChoice=tieChoice_priority)

    #p2 = Human('ALEX')
    #p2 = AI('CELLS2', controlled_cells, 5, tieChoice=tieChoice_priority)
    p2 = AI('SOLS2', controlled_sols, 3, tieChoice=tieChoice_priority)
    #p2 = AI('RANDOM2', random_move)
    #p2 = AI('HYBRID2', cell_sol_hybrid, 3, tieChoice=tieChoice_priority)
    player_pair = (p1, p2)
    game = Game(player_pair)

    winType = game.checkWin()
    count = 0
    while not winType:
        print()
        game.drawScreen()
        #print("\n" + str(controlled_cells(game.getState())))
        mv = game.getCurPlayer().choose_move(game.getState())
        print(mv)
        game.update(mv)
        winType = game.checkWin()
        count += 1

    if winType == const.DRAW_VAL:
        msg = "The game was a draw!"
    else:
        msg = str(game._winner) + " wins!"
    game.drawScreen(msg)

def main():
    cur_state = SystemState()
    valid = False
    prevMv = Move()
    is_goal = False
    winner = 2
    while not is_goal:
        for i in range (1,4):
            #if i != 2:
                #val = printState (cur_state, "input action (flip/none): ", True).strip().split(' ')
            #    val = printState (cur_state, "input action (flip/none): ", True)
            #    key = val[0]
            #    pos = -1
            #else:
                #val = printState (cur_state, "input action (place [1-7]): ", True).strip().split(' ')
            val = printState (cur_state, "input action (place [1-7]): ", True)
            print(val)
            key = 'place'
            pos = (inival)-1
            move = Move(key, cur_state._player, pos)
            prevMv = move
            valid = cur_state.validMove(move)
            if valid:
                print("move is valid")
                cur_state = cur_state.update(move)
                is_goal, winner = cur_state.isGoal()
                if is_goal:
                    break
            else:
                move = Move('None', cur_state._player, -1)
                prevMv = move
                cur_state = cur_state.update(move)
                is_goal, winner = cur_state.isGoal()
                if is_goal:
                    break
    if winner == 0 or winner == 1:
        win_string = 'A' if winner == 0 else 'B' if winner == 1 else '-'
        printState (cur_state,'Player %s wins!' %win_string)
    else:
        printState (cur_state,'Draw!')

if __name__ == "__main__":
    #test()
    main2()
