import mancala

if __name__ == "__main__":
    board = mancala.Board()

    board.keepOpen()
    turn = board.getTurn()
    if turn == mancala.Turn.P1:
        board.P1Move(0)
    else:
        board.P2Move(5)

    while True:
        board.keepOpen()
