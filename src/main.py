import const

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

def promptPlayers():
    ptype = [None, None]

    name_mapping = ['HUMAN', 'SOLS', 'CELLS', 'HYBRID', 'RANDOM']
    ptype[0] = input("Enter Player 1 type: [1: Human], [2: Sols], [3: Cells], [4: Hybrid], [5: Random]")
    ptype[1] = input("Enter Player 2 type: [1: Human], [2: Sols], [3: Cells], [4: Hybrid], [5: Random]")
    for i in range(len(ptype)):
        if ptype[i].isnumeric():
            ptype[i] = name_mapping[int(ptype[i])-1]
        else:
            ptype[i] = ptype[i].upper()

    pname = [ptype[0]+'1', ptype[1]+'2']
    pclass = [AI, AI]
    pfunc = [None, None]
    for i in range(2):
        if ptype[i] == "RANDOM" or ptype[i] == "5":
            pfunc[i] = random_move
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
    else:
        p1 = pclass[0](pname[0], pfunc[0], const.NUM_LOOK, tieChoice=tieChoice_priority)

    if pclass[1] == Human:
        p2 = pclass[1](pname[1])
    else:
        p2 = pclass[1](pname[1], pfunc[1], const.NUM_LOOK, tieChoice=tieChoice_priority)

    return (p1, p2)

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
    const.NUM_LOOK = 3

    num_games = 5

    player_pair = promptPlayers()
    play_again = True

    stats = {}
    stats['results'] = [0, 0, 0]

    for i in range(num_games):
        game = Game(player_pair)
        stats['game'] = game

        while not game._gameEnd:
            game.drawScreen()
            mv = game.getCurPlayer().choose_move(game.getState())

            game.update(mv)
            game.checkWin()

        game.log("test.txt")
        if game._winner is None:
            msg = "The game was a draw!"
            stats['results'][2] += 1
        else:
            msg = str(game._winner) + " wins!"
            stats['results'][game._player_pair.index(game._winner)] += 1
        game.drawScreen(msg)

        #play_again = promptContinue(stats)


if __name__ == "__main__":
    #test()
    main()
