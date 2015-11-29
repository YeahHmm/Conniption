from itertools import repeat
from copy import deepcopy

NUM_COLS = 7    # Width of board
NUM_ROWS = 6    # Height of board

MAX_FLIPS = 4   # Max flips per player per game
NUM_STAGES = 3

WIN_VAL = 1     # Key representing 
EMPTY_VAL = 2   # Key representing empty cells

LEN_SOL = 4     # Length of winning chain

SOLS_GRAPH = None   # Graph of cell adjacencies between solution positions
CELL_MAP = {}       # Dictionary mapping cells to sets of solutions

NUM_LOOK = 3
DEBUG = False
