import heapq
import random
from itertools import product, starmap

import const
from resource import Node


'''
A tie breaker that sorts none Moves before place Moves and place Moves before
flip Moves. Thus the AI will slightly prefer doing nothing to flipping. Place
Moves are randomly sorted.
'''
def tieChoice_priority(node_list, get_max=True):
    # Sort based on minimizing or maximizing
    node_list.sort(reverse=not get_max)
    # Functions to assign weights to Move objects. Lower is preferred.
    weight = {'none': lambda mv: -1,
            'place': lambda mv: random.randint(0, const.NUM_COLS),
            'flip':lambda mv: const.NUM_COLS
        }
    # Get the best Move objects, and assign new weights based on Move type
    first = node_list.pop()
    best = [Node(weight[first._item._action](first._item), first)]
    best_val = best[0]._item._value

    while len(node_list) > 0 and node_list[-1]._value == best_val:
        node = node_list.pop()
        mv = node._item
        heapq.heappush(best, Node(weight[mv._action](mv), node))
    # Choose the Move with the smallest weight
    smallest = heapq.heappop(best)._item
    return smallest._item

'''
Same logic as the above tiebreaker, returns a Node object
in order to use the value in the Qlearn function
'''

def tieChoice_priority_qlearn(node_list, get_max):
        # Sort based on minimizing or maximizing
        node_list.sort(reverse=not get_max)
        print (node_list)
        # Functions to assign weights to Move objects. Lower is preferred.
        weight = {'none': lambda mv: -1,
                'place': lambda mv: random.randint(0, const.NUM_COLS),
                'flip':lambda mv: const.NUM_COLS
            }
        #print(node_list)
        best = [Node(weight[x._item._action](x._item), x._item) for x in node_list]
        return best

'''
Uses const.SOLS_GRAPH to perform calculation. A player's score is based on
how many solutions he has control over and how much control he has over each.
Empty or shared solutions have a score of 0. Player 2's score is subtracted
from Player 1's.
'''
def controlled_sols(state):
    board = state.filledMatrix()
    sgraph = const.SOLS_GRAPH
    sdict = {s : True for s in sgraph.getVertices()}

    zoneCounts = [[0]*4, [0]*4]
    for sol in sdict:
        # Skip flagged solutions
        if not sdict[sol]:
            continue

        # Find unique values in solution's cells
        vals = set(map(lambda p: board[p[0]][p[1]], sol))

        if const.EMPTY_VAL in vals:
            # Flag solution if it is completely empty
            if len(vals) == 1:
                sdict[sol] = False
                continue
            # Remove const.EMPTY_VAL if solution is not empty
            else:
                vals.remove(const.EMPTY_VAL)

        # Flag solutions containing different tiles
        if 0 in vals and 1 in vals:
            vals_max = list(filter(lambda p: board[p[0]][p[1]] == 0, sol))
            vals_min = list(filter(lambda p: board[p[0]][p[1]] == 1, sol))

            for pair in map(lambda p: tuple(sorted(p)), \
                    product(vals_max, vals_min)):
                for s in sgraph.neighbors(sol, pair):
                    sdict[s] = False
            continue

        # Get player that controls the solution and count number of tiles
        # in the solution
        player = list(vals)[0]
        numPlaced = len(list(filter(lambda p: board[p[0]][p[1]] != 2, sol)))

        # Increment the appropriate counter
        zoneCounts[player][numPlaced-1] += 1

    # Assign the weights for the number of tiles controlling a solution
    weights = [1, 4, 16, 1024]
    zoneCounts[0] = list(map(lambda p: p[0]*p[1], zip(zoneCounts[0], weights)))
    zoneCounts[1] = list(map(lambda p: p[0]*p[1], zip(zoneCounts[1], weights)))

    # Return the difference between the two scores
    return sum(zoneCounts[0]) - sum(zoneCounts[1])


'''
Score a SystemState based on the value of each owned cell. The value of a cell
is equal to the number of solutions which contain it. A player's score is the
sum of the values of controlled cells. Player 2's score is subtracted from
Player 1's.
'''
def controlled_cells(state):
    board = state.filledMatrix()

    # Iterate over the board's cells
    vals = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            # Multiply the cell's value by 1 if it is owned by Player 1
            # Multiply by -1 if owned by Player 2
            # Multiply by 0 if empty
            pmod = 1 if board[i][j] == 0 else -1 if board[i][j] == 1 else 0

            # Add the modified value to a list
            vals.append(pmod * len(const.CELL_MAP[(i, j)]))

    # Return the sum of modified values
    return sum(vals)

'''
Use both Controlled Cells and Controlled Solutions. Given a SystemState,
calculate both scores and add them together.
'''
def cell_sol_hybrid(state):
    cell_val = controlled_cells(state)
    sol_val = controlled_sols(state)
    return cell_val + sol_val

def flip_bias_hybrid(state):
    val = cell_sol_hybrid(state)
    bias = 10
    p1_bias = -bias * state._num_flips[0]
    p2_bias = bias * state._num_flips[1]

    return val + p1_bias + p2_bias

'''
Assign a random score from 0 to 9.
'''
def random_move(state):
    return random.randint(0, 10)
