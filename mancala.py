"""
Board for the Mancala game (2 Players).

Author: Jack Stettner
Date: 12 November 2018
"""
import pygame
from enum import Enum

class Turn(Enum):
    P1 = 1
    P2 = 2

class Board(object):
    """
        Mancala Board Class

        Attributes:
        _turn: Turn
        _tiles: [int], length 14, starting from p2 GOAL, going counter-clockwise
    """
    TILE_POSITIONS = [(70, 145), (175, 270), (290, 270), (395, 270), (505, 270), (615, 270), (720, 270), (830,200), (720, 80), (615, 80), (505, 80), (395, 80), (290, 80), (175, 80)]
    STARTING_BOARD = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Mancala')

        self._tiles = self.STARTING_BOARD
        self._turn = Turn.P1

        self._gameDisplay = pygame.display.set_mode((900, 354))
        clock = pygame.time.Clock()

        crashed = False

        self._board_img = pygame.image.load('assets/board.png')
        self._board_img = pygame.transform.scale(self._board_img, (900, 354))
        self._gameDisplay.blit(self._board_img, (0, 0))

        self.updateTileUI()
        pygame.display.update()

    def keepOpen(self):
        pygame.event.get()

    def updateTileUI(self):
        self._gameDisplay.blit(self._board_img, (0, 0))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)

        for tile_index in range(len(self._tiles)):
            self._gameDisplay.blit(myfont.render(str(self._tiles[tile_index]), False, (255, 255, 255)), self.TILE_POSITIONS[tile_index])

        pygame.display.update()

    def getTurn(self):
        return self._turn

    def P1View(self):
        return self._tiles

    def P2View(self):
        return self._tiles[6:] + self._tiles[:6]

    def P1Move(self, tile_index):
        assert isinstance(tile_index, int)
        assert tile_index >= 0 and tile_index < 6
        assert self._turn == Turn.P1

        stones = self._tiles[tile_index + 1]

        for i in range(stones + 1):
            self._tiles[((tile_index + 1) + i) % len(self._tiles)] += 1

        self._tiles[tile_index + 1] -= stones

        self.updateTileUI()
        return self.P1View()

    def P2Move(self, tile_index):
        assert isinstance(tile_index, int)
        assert tile_index >= 0 and tile_index < 6
        assert self._turn == Turn.P2

        tile_index += 7

        stones = self._tiles[tile_index+1]

        for i in range(stones + 1):
            self._tiles[((tile_index + 1) + i) % len(self._tiles)] += 1

        self._tiles[tile_index + 1] -= stones

        self.updateTileUI()
        return self.P2View()

    # def start(self):
    #     gameDisplay = pygame.display.set_mode((900, 354))
    #     clock = pygame.time.Clock()
    #
    #     crashed = False
    #
    #     board = pygame.image.load('assets/board.png')
    #     board = pygame.transform.scale(board, (900, 354))
    #     gameDisplay.blit(board, (0, 0))

        # while not crashed:
        #     pygame.event.get()
        #     # one round of turns from each player
        #     self.updateTileUI(gameDisplay)
        #
        #     # for event in pygame.event.get():
        #     #     if event.type == pygame.QUIT:
        #     #         crashed = True
        #     #
        #     #     print(event)
        #
        #     pygame.display.update()
        #     clock.tick(60)
