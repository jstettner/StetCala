"""
Test Procedure for the Mancala Board class

Plays random moves until the game is complete and then prints the score.

Author: Jack Stettner
Date: 12 November 2018
"""

import mancala
import random

if __name__ == "__main__":
    board = mancala.Board(True)

    while board.checkEmpty() == False:
        turn = board.getTurn()
        if turn == mancala.Turn.P1:
            board.P1Move(random.randint(0,5))
        else:
            board.P2Move(random.randint(0,5))

    print(board.getScore())
