"""
Procedure that allows the user to play against a saved model.

Author: Jack Stettner
Date: 15 November 2018
"""
import neat
import pickle
import mancala
import numpy as np

if __name__ == '__main__':
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    board = mancala.Board(True)

    while board.checkEmpty() == False:
        turn = board.getTurn()
        if turn == mancala.Turn.P1:
            while True:
                try:
                    move = int(input('Enter move [0..5]: '))
                    assert move >= 0 and move <= 5
                    break
                except (AssertionError, ValueError):
                    print('Invalid input. Try again.')

            board.P1Move(move)
        else:
            obs = board.P2View()
            action = model.activate(obs)
            action = np.argmax(action)
            board.P2Move(int(action))
            print('Opponent chose ',action)

    print(board.getScore())
