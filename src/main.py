import const
import sys
#sys.setrecursionlimit(10000)

from evaluation import *
from game import Game, Human, AI
from printing import prompt
from resource import Move
from reinforce import Qlearn, MinimaxQlearn

# Testing function to more concisely build a board
def place(game, player, col):
    game.update(Move('none', player))
    game.update(Move('place', player, col))
    game.update(Move('none', player))

# Testing method
def test():
    const.DEBUG = True
    ai1 = Human('P1')
    ai2 = Human('P2')
    player_pair = (ai1, ai2)
    game = Game(player_pair)

    f = open('fail.txt')
    lf = [l.strip() for l in f]
    last = lf[-1]
    seq = map(lambda s: s.strip('()').split(', '), last.split('),('))
    mv_list = list(map(lambda t: Move(t[0].strip("'"), int(t[1]), int(t[2])), seq))

    game.drawScreen()
    for mv in mv_list:
        game.update(mv)
        game.drawScreen()
        print(game.checkWin())

# Prompt for player types and names
def promptPlayers(in_pair=None):
    ptype = [None, None]
    name_mapping = ['HUMAN', 'SOLS', 'CELLS', 'HYBRID', 'FLIP', 'RANDOM', 'QLEARN', 'MINIMAXQLEARN']
    if in_pair != None:
        ptype = list(in_pair)
    else:
        prompt_string = "Enter Player 1 type: \n\t[1: Human], \n\t[2: Sols]," \
                        + "\n\t[3: Cells],\n\t[4: Hybrid],\n\t[5: Flip]," \
                        + "\n\t[6: Random] \n\t[7: QLearn]\n\t[8: MinimaxQlearn]\nChoose: "
        ptype[0] = input(prompt_string)
        ptype[1] = input(prompt_string)

    for i in range(len(ptype)):
        if ptype[i].isnumeric():
            ptype[i] = name_mapping[int(ptype[i])-1]
        else:
            ptype[i] = ptype[i].upper()

    pname = [ptype[0]+'1', ptype[1]+'2']
    pclass = [AI, AI]
    pfunc = [None, None]
    for i in range(2):
        if ptype[i] == "RANDOM" or ptype[i] == "6":
            pfunc[i] = random_move
        elif ptype[i] == "QLEARN" or ptype[i] == "7":
            pfunc[i] = flip_bias_hybrid
            pclass[i] = Qlearn
        elif ptype[i] == "MINIMAXQLEARN" or ptype[i] == "8":
            pfunc[i] = flip_bias_hybrid
            pclass[i] = MinimaxQlearn
        elif ptype[i] == "FLIP" or ptype[i] == "5":
            pfunc[i] = flip_bias_hybrid
        elif ptype[i] == "CELLS" or ptype[i] == "3":
            pfunc[i] = controlled_cells
        elif ptype[i] == "SOLS" or ptype[i] == "2":
            pfunc[i] = controlled_sols
        elif ptype[i] == "HYBRID" or ptype[i] == "4":
            pfunc[i] = cell_sol_hybrid
        elif ptype[i] == "HUMAN" or ptype[i] == "1":
            pclass[i] = Human
            pname[i] = input("Enter Player %d name: " % (i+1))

    if pclass[0] == Human:
        p1 = pclass[0](pname[0])
    elif pclass[0] == Qlearn:
        p1 = pclass[0](pname[0], pfunc[0],tieChoice=tieChoice_priority_qlearn, \
            learning=True)
    elif pclass[0] == MinimaxQlearn:
        p1 = pclass[0](pname[0], pfunc[0], const.NUM_LOOK, tieChoice=tieChoice_priority_qlearn, \
            learning=True)
    elif pfunc[0] == random_move:
        p1 = pclass[0](pname[0], pfunc[0], 1, tieChoice=tieChoice_priority)
    else:
        p1 = pclass[0](pname[0], pfunc[0], const.NUM_LOOK, tieChoice=tieChoice_priority)

    if pclass[1] == Human:
        p2 = pclass[1](pname[1])
    elif pclass[1] == Qlearn:
        p1 = pclass[1](pname[1],pfunc[0],tieChoice=tieChoice_priority_qlearn,\
            learning=True)
    elif pclass[1] == MinimaxQlearn:
        p2 = pclass[1](pname[1], pfunc[1], const.NUM_LOOK, tieChoice=tieChoice_priority_qlearn, \
            learning=True)
    elif pfunc[1] == random_move:
        p2 = pclass[1](pname[1], pfunc[1], 1, tieChoice=tieChoice_priority)
    else:
        p2 = pclass[1](pname[1], pfunc[1], const.NUM_LOOK, tieChoice=tieChoice_priority)

    return (p1, p2)

# Ask if supervisor wants to run another game
def promptContinue(stats, msg=''):
    p1 = stats['game']._player_pair[0]
    p2 = stats['game']._player_pair[1]
    results = stats['results']
    msg = '\n' + msg + '\n'
    msg += str(p1) + ': ' + '/'.join(map(str, results))
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

# Primary game loop
def main():
    # Set player types and logging if provided in command line
    if len(sys.argv) == 4:
        pair = (sys.argv[1], sys.argv[2])
        save_file = sys.argv[3]
    else:
        pair = None
        save_file = "save.pkl"

    # Config info for debugging or game tweaking
    const.DEBUG = False
    const.MAX_FLIPS = 4
    const.NUM_LOOK = 3

    num_games = 100

    player_pair = promptPlayers(pair)
    play_again =  False

    stats = {}
    stats['results'] = [0, 0, 0]

    for _ in range(num_games):
    #while play_again:
        # Begin new game
        game = Game(player_pair)
        stats['game'] = game

        # Play until game ends
        while not game.checkWin():
            game.drawScreen()
            mv = game.getCurPlayer().choose_move(game.getState())
            #print (mv.__hash__())
            game.update(mv)
        if game.getCurPlayer()._name == 'QLEARN1':
            print (game.getCurPlayer().Q)
        # Log moves and results with pickle
        game.save(save_file)

        # Prompt for replay
        if game._winner is None:
            msg = "The game was a draw!"
            stats['results'][2] += 1
        else:
            msg = str(game._winner) + " wins!"
            stats['results'][game._player_pair.index(game._winner)] += 1

    play_again = promptContinue(stats, msg)

if __name__ == "__main__":
    #test()
    main()
