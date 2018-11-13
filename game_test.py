import mancala

if __name__ == "__main__":
    board = mancala.Board()

    board.keepOpen()
    turn = board.getTurn()
    if turn == mancala.Turn.P1:
        print(board.P1Move(5))
    else:
        board.P2Move(5)

    while True:
        board.keepOpen()
