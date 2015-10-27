from printFunction import printboard
from resource import SystemState
from resource import Move

def main():
    print("Start Main")
    board = "0"*42
    currentState = SystemState()
    matrix = list(map(int, list(board)))
    printboard(matrix)

    position = input("input move (1-7): ")
    move = Move('place',0,position)
    currentState = currentState.update(move)
    matrix = list(map(int, list(board)))
    printboard(matrix)

if __name__ == "__main__":
    main()
