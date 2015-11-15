from itertools import repeat
from copy import deepcopy

NUM_COLS = 7    # Width of board
NUM_ROWS = 6    # Height of board

MAX_FLIPS = 4   # Max flips per player per game
NUM_STAGES = 3

EMPTY_VAL = 2   # Key representing empty cells

LEN_SOL = 4     # Length of winning chain
WIN_VAL = 1     # Value for a game won
DRAW_VAL = 2    # Value for a draw game

SOLS_GRAPH = None   # Graph of adjacencies between solution positions
# Grid recording number of solutions in each cell
SOL_DENSITY = []
for i in range(NUM_COLS):
    SOL_DENSITY.append([0] * NUM_ROWS)

DEBUG = False
