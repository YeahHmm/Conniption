import os

from printFunction import printboard
from resource import SystemState
from resource import Move

def main():
    cur_state = SystemState()

    while True:
        os.system('clear')
        print (cur_state)
        key = input("input action (flip, place): ").strip()
        if key == 'place':
            position = int(input("input move (1-7): ").strip()) - 1
            move = Move(key, cur_state._cur_player, position)
        else:
            move = Move(key, cur_state._cur_player)

        if cur_state.validMove(move):
            cur_state = cur_state.update(move)
        print (cur_state)

if __name__ == "__main__":
    main()
