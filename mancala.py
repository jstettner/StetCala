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
    STARTING_BOARD = [0, 4, 4, 4, 4, 0, 4, 0, 4, 4, 4, 4, 4, 4]
    P1_GOAL = 7
    P2_GOAL = 0

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

    def P1Empty(self):
        tiles = [1, 2, 3, 4, 5, 6]
        empty = True

        for index in tiles:
            if self._tiles[index] > 0:
                empty = False
        return empty

    def P2Empty(self):
        tiles = [8, 9, 10, 11, 12, 13]
        empty = True

        for index in tiles:
            if self._tiles[index] > 0:
                empty = False
        return empty

    def checkEmpty(self):
        if self.P1Empty():
            for i in [8, 9, 10, 11, 12, 13]:
                val = self._tiles[i]
                self._tiles[i] = 0
                self._tiles[self.P1_GOAL] += val

        if self.P2Empty():
            for i in [1, 2, 3, 4, 5, 6]:
                val = self._tiles[i]
                self._tiles[i] = 0
                self._tiles[self.P2_GOAL] += val

        if self.P1Empty() or self.P2Empty():
            return True
        return False

    def P1Move(self, tile_index):
        assert isinstance(tile_index, int)
        assert tile_index >= 0 and tile_index < 6
        assert self._turn == Turn.P1

        tile_index += 1

        stones = self._tiles[tile_index]
        self._tiles[tile_index] = 0

        i = 0
        place = tile_index
        while stones > 0:
            i += 1
            place = (tile_index + i) % len(self._tiles)

            if place == self.P2_GOAL: # skip enemy goals
                i += 1

            self._tiles[place] += 1
            stones -= 1

        if place == self.P1_GOAL:
            self._turn = Turn.P1
        else:
            self._turn = Turn.P2

        if place in [1, 2, 3, 4, 5, 6] and self._tiles[place] == 1:
            self._tiles[place] = 0
            self._tiles[self.P1_GOAL] += 1

            self._tiles[self.P1_GOAL] += self._tiles[len(self._tiles) - place]
            self._tiles[len(self._tiles) - place] = 0

        self.updateTileUI()
        return self.P1View(), self.checkEmpty()

    def P2Move(self, tile_index):
        assert isinstance(tile_index, int)
        assert tile_index >= 0 and tile_index < 6
        assert self._turn == Turn.P2

        tile_index += 8

        stones = self._tiles[tile_index]
        self._tiles[tile_index] = 0

        i = 0
        place = tile_index
        while stones > 0:
            i += 1
            place = (tile_index + i) % len(self._tiles)

            if place == self.P2_GOAL: # skip enemy goals
                i += 1

            self._tiles[place] += 1
            stones -= 1

        if place == self.P2_GOAL:
            self._turn = Turn.P2
        else:
            self._turn = Turn.P1

        if place in [8, 9, 10, 11, 12, 13] and self._tiles[place] == 1:
            self._tiles[place] = 0
            self._tiles[self.P2_GOAL] += 1

            self._tiles[self.P2_GOAL] += self._tiles[len(self._tiles) - place]
            self._tiles[len(self._tiles) - place] = 0

        self.updateTileUI()
        return self.P2View(), self.checkEmpty()
