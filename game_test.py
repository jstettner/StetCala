"""
Test Procedure for the Mancala Board class

Plays random moves until the game is complete and then prints the score.

Author: Jack Stettner
Date: 12 November 2018
"""

import mancala
import random

if __name__ == "__main__":
    board = mancala.Board(False)

    while board.checkEmpty() == False:
        turn = board.getTurn()
        if turn == mancala.Turn.P1:
            # move = input('P1 Move: ')
            board.P1Move(random.randint(0,5))
        else:
            # move = input('P2 Move: ')
            board.P2Move(random.randint(0,5))

    # print(board.P1View())
    print(board.getScore())
