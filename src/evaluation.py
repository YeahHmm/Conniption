import heapq
import random
from itertools import product, starmap

import const
from resource import Node

def tieChoice_priority(node_list, get_max=True):
    print(node_list)
    node_list.sort(reverse=not get_max)

    weight = {'none': lambda mv: -1,
            'place': lambda mv: random.randint(0, const.NUM_COLS),
            'flip':lambda mv: const.NUM_COLS
        }

    first = node_list.pop()
    best = [Node(weight[first._item._action](first._item), first)]
    best_val = best[0]._item._value

    while len(node_list) > 0 and node_list[-1]._value == best_val:
        node = node_list.pop()
        mv = node._item
        print(weight[mv._action](mv))
        heapq.heappush(best, Node(weight[mv._action](mv), node))

    print(best)
    return heapq.heappop(best)._item._item

def controlled_sols(state):
    board = state.filledMatrix()
    sgraph = const.SOLS_GRAPH
    sdict = {s : True for s in sgraph.getVertices()}

    zoneCounts = [[0]*4, [0]*4]
    for sol in sdict:
        if not sdict[sol]:
            continue

        vals = set(map(lambda p: board[p[0]][p[1]], sol))

        if 2 in vals:
            if len(vals) == 1:
                sdict[sol] = False
                continue
            else:
                vals.remove(2)

        if 0 in vals and 1 in vals:
            vals_max = list(filter(lambda p: board[p[0]][p[1]] == 0, sol))
            vals_min = list(filter(lambda p: board[p[0]][p[1]] == 1, sol))

            for pair in map(lambda p: tuple(sorted(p)), \
                    product(vals_max, vals_min)):
                for s in sgraph.neighbors(sol, pair):
                    sdict[s] = False
            continue

        player = list(vals)[0]
        numPlaced = len(list(filter(lambda p: board[p[0]][p[1]] != 2, sol)))
        zoneCounts[player][numPlaced-1] += 1

    #print("Weights:", zoneCounts)
    weights = [1, 4, 8, 1024]
    zoneCounts[0] = list(map(lambda p: p[0]*p[1], zip(zoneCounts[0], weights)))
    zoneCounts[1] = list(map(lambda p: p[0]*p[1], zip(zoneCounts[1], weights)))

    return sum(zoneCounts[0]) - sum(zoneCounts[1])

def controlled_cells(state):
    board = state.filledMatrix()

    vals = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            pmod = 1 if board[i][j] == 0 else -1 if board[i][j] == 1 else 0
            vals.append(pmod * len(const.CELL_MAP[(i, j)]))

    return sum(vals)

def cell_sol_hybrid(state):
    cell_val = controlled_cells(state)
    sol_val = controlled_sols(state)
    return cell_val + sol_val

def random_move(state):
    return random.randint(0, 10)
