"""
Test Procedure for the Mancala Board class

Plays random moves until the game is complete and then prints the score.

Author: Jack Stettner
Date: 12 November 2018
"""

from Mancala import mancala
import random

def test(vis=True):
    board = mancala.Board(vis)

    while board.checkEmpty() == False:
        turn = board.getTurn()
        if turn == mancala.Turn.P1:
            board.P1Move(random.randint(0,5))
        else:
            board.P2Move(random.randint(0,5))

    print(board.getScore())
