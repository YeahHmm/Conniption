import os
from termcolor import colored

from printFunction import printboard
from resource import SystemState
from resource import Move

def printState(state, prompt='', inp=False):
    os.system('clear')
    toPrint = ' '
    for i in range(SystemState.NUM_COLS):
        toPrint += '{0:^7} '.format(i+1)
    print (toPrint)
    print (state)
    print (colored('Player A: ', 'cyan') + colored('* * * *', 'green', attrs=['bold']))
    print (colored('Player B: ', 'white') + colored('* * * *', 'green', attrs=['bold']))
    if prompt != '' and inp:
        return input(colored(prompt, 'yellow', attrs=['bold']))
    elif prompt != '' and not inp:
        return print(prompt)

def main():
    cur_state = SystemState()
    valid = False
    prevMv = Move()
    is_goal = False
    winner = 2
    while not is_goal:
        for i in range (1,4):
            if i != 2:
                val = printState (cur_state, "input action (flip/none): ", True).strip().split(' ')
                key = val[0]
                pos = -1
            else:
                val = printState (cur_state, "input action (place [1-7]): ", True).strip().split(' ')
                key = 'place'
                pos = int(val[-1]) - 1
            move = Move(key, cur_state._player, pos)
            prevMv = move
            valid = cur_state.validMove(move)
            if valid:
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
    main()
