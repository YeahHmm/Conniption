import os

from termcolor import colored
from getch import _Getch

from resource import SystemState

def printState(state, prompt='', inp=False):
    os.system('clear')
    toPrint = ' '
    for i in range(SystemState.NUM_COLS):
        toPrint += '{0:^7} '.format(i+1)
    print(toPrint)
    print(state)
    print(colored('Player A: ', 'cyan') + colored('* * * *', 'green', attrs=['bold']))
    print(colored('Player B: ', 'white') + colored('* * * *', 'green', attrs=['bold']))
    if prompt != '' and inp:
        #inKey = _Getch()
        #import sys
        #key = inKey()
        #print(key)
        print('Press a key')
        inkey = _Getch()
        key = inkey()
        if key not in map(str, range(1,8)):
            return key
        else:
            return key
        #return input(colored(prompt, 'yellow', attrs=['bold']))
    elif prompt != '' and not inp:
        return print(prompt)
