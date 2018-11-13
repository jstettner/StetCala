import mancala
import random

if __name__ == "__main__":
    board = mancala.Board(True)

    while board.checkEmpty() == False:
        turn = board.getTurn()
        if turn == mancala.Turn.P1:
            # move = input('P1 Move: ')
            print(board.P1Move(random.randint(0,5)))
        else:
            # move = input('P2 Move: ')
            print(board.P2Move(random.randint(0,5)))

    print(board.P1View())
    print(board.getScore())
