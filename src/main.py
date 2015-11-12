from printing import printState
from resource import SystemState
from resource import Move


def main():
    cur_state = SystemState()
    valid = False
    prevMv = Move()
    is_goal = False
    winner = 2
    while not is_goal:
        for i in range (1,4):
            #if i != 2:
                #val = printState (cur_state, "input action (flip/none): ", True).strip().split(' ')
            #    val = printState (cur_state, "input action (flip/none): ", True)
            #    key = val[0]
            #    pos = -1
            #else:
                #val = printState (cur_state, "input action (place [1-7]): ", True).strip().split(' ')
            val = printState (cur_state, "input action (place [1-7]): ", True)
            print(val)
            key = 'place'
            pos = int(val)-1
            move = Move(key, cur_state._player, pos)
            prevMv = move
            valid = cur_state.validMove(move)
            if valid:
                print("move is valid")
                cur_state = cur_state.update(move)
                is_goal, winner = cur_state.isGoal()
                if is_goal:
                    break
            else:
                move = Move('None', cur_state._player, -1)
                prevMv = move
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
