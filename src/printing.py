import os
import sys

from termcolor import colored
from getch import _Getch

import const


def printState(state, msg='', is_prompt=False):
    os.system('clear')
    toPrint = ' '
    for i in range(const.NUM_COLS):
        toPrint += '{0:^7} '.format(i+1)
    print(toPrint)
    print(state)

    print(colored('Player A: ', 'cyan') + colored('* * * *', 'green', attrs=['bold']))
    print(colored('Player B: ', 'white') + colored('* * * *', 'green', attrs=['bold']))
    if msg != '' and is_prompt:
        #inKey = _Getch()
        #import sys
        #key = inKey()
        #print(key)
        print(msg)
        inkey = _Getch()
        key = inkey()
        if key is not '\x03':
            return key
        else:
            raise KeyboardInterrupt
        #return is_promptut(colored(msg, 'yellow', attrs=['bold']))
    elif msg != '' and not is_prompt:
        print(msg)

def prompt(msg):
    sys.stdout.write('\r' + msg)
    inkey = _Getch()
    key = inkey()
    if key is not '\x03':
        return key
    else:
        raise KeyboardInterrupt
