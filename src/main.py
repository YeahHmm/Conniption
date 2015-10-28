import os

from printFunction import printboard
from resource import SystemState
from resource import Move

def main():
    cur_state = SystemState()

    while True:
        os.system('clear')
        print (cur_state)
        val = input("input action (flip, place [1-7]): ").strip().split(' ')
        key = val[0]
        pos = -1
        if len(val) == 2:
            pos = int(val[1]) - 1
        move = Move(key, cur_state._cur_player, pos)
        if cur_state.validMove(move):
            cur_state = cur_state.update(move)
        print (cur_state)

if __name__ == "__main__":
    main()
