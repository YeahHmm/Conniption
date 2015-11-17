import os
import sys

from termcolor import colored
from getch import _Getch

import const


def prompt(msg):
    sys.stdout.write('\r' + msg)
    inkey = _Getch()
    key = inkey()
    if key == '\x03':
        raise KeyboardInterrupt
    else:
        return key
