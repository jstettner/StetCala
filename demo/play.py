"""
Procedure that allows the user to play against a saved model.

Author: Jack Stettner
Date: 15 November 2018
"""
import neat
import pickle
import os
from Mancala import mancala
import numpy as np
import pygame

local_dir = os.path.dirname(__file__)

def print_rules():
    print('Each player has 6 regular tiles and 1 \'Mancala\'.')
    print('One your turn, you can select a tile. All stones inside will be moved counter-clockwise and dropped one by one.')
    print('Stones may deposit into your own Mancala on your turn, but they skip your opponents.')
    print('If the final stone from your move lands in an empty tile, that stone and any stones opposing it are moved into your Mancala.')
    print('If the final stone lands into your Mancala, you get another turn.')
    print('When one side is empty, the other side\'s stones move to their Mancala and the score is tallied.')


def play(model):
    model_path = os.path.join(local_dir, model)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    board = mancala.Board(True)

    print_rules()

    while board.checkEmpty() == False:
        turn = board.getTurn()
        if turn == mancala.Turn.P1:
            move = None
            while move == None:
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()

                        # get a list of all sprites that are under the mouse cursor
                        clicked_sprites = [s for s in board.getSprites() if s.b.collidepoint(pos)]
                        # print(clicked_sprites)
                        try:
                            # move = int(input('Enter move [0..5]: '))
                            move = clicked_sprites[0].number
                            assert move >= 0 and move <= 5
                            break
                        except (AssertionError, ValueError, IndexError):
                            move = None
                            print('Invalid input. Try again.')
            board.P1Move(move)
        else:
            obs = board.P2View()
            action = model.activate(obs)
            action = np.argmax(action)
            board.P2Move(int(action))
            print('Opponent chose ',action)

    player_score, bot_score = board.getScore()
    print('Player Score: {player_score}, StetCala: {bot_score}'.format(player_score=player_score, bot_score=bot_score))
    if player_score == bot_score:
        print('You tied.')
    elif player_score > bot_score:
        print('You beat StetCala!')
    else:
        print('You lost. Another soul added to the collection by StetCala.')
