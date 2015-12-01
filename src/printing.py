import os
import sys

from termcolor import colored
from getch import _Getch

import const


'''
Print a message to the screen and use getch to capture key presses. Throw a
keyboard interruption on ctrl+c
'''
def prompt(msg):
    sys.stdout.write('\r' + msg)
    inkey = _Getch()
    key = inkey()
    if key == '\x03':
        raise KeyboardInterrupt
    else:
        return key
