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
    TIE = 0

class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width, height, x, y, number):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill((255, 0, 0))
       self.x = x
       self.y = y
       self.number = number

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

    def draw(self, screen):
        self.b = screen.blit(self.image, (self.x, self.y))

    # def getImage(self):
    #     return self.image

class Board(object):
    """
        Mancala Board Class

        Attributes:
        _turn: Turn
        _tiles: [int], length 14, starting from p2 GOAL, going counter-clockwise
        _visible: whether or not the board shows (changes run-speed)
    """
    TILE_POSITIONS = [(70, 145), (175, 270), (290, 270), (395, 270), (505, 270), (615, 270), (720, 270), (830,200), (720, 80), (615, 80), (505, 80), (395, 80), (290, 80), (175, 80)]
    STARTING_BOARD = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
    SPRITES = [(150, 245), (265, 245), (370, 245), (480, 245), (590, 245), (695, 245)]
    P1_GOAL = 7
    P2_GOAL = 0

    def __init__(self, visible=True):
        assert isinstance(visible, bool)

        self._visible = visible

        self.reset()

        self._turn = Turn.P1

        if self._visible:
            pygame.init()
            pygame.font.init()
            pygame.display.set_caption('Mancala')

            self._gameDisplay = pygame.display.set_mode((900, 354))
            clock = pygame.time.Clock()

            crashed = False

            self._board_img = pygame.image.load('assets/board.png')
            self._board_img = pygame.transform.scale(self._board_img, (900, 354))
            self._gameDisplay.blit(self._board_img, (0, 0))

            self._sprites = []
            for i in range(len(self.SPRITES)):
                self._sprites.append(Block(20, 20, self.SPRITES[i][0], self.SPRITES[i][1], i))

            self.updateTileUI()
            pygame.display.update()

    def getSprites(self):
        return self._sprites

    def reset(self):
        self._tiles = []
        for tile in self.STARTING_BOARD:
            self._tiles.append(tile)

    def keepOpen(self):
        if self._visible:
            pygame.event.get()

    def updateTileUI(self):
        if self._visible:
            self._gameDisplay.blit(self._board_img, (0, 0))
            myfont = pygame.font.SysFont('Comic Sans MS', 30)

            for tile_index in range(len(self._tiles)):
                self._gameDisplay.blit(myfont.render(str(self._tiles[tile_index]), False, (255, 255, 255)), self.TILE_POSITIONS[tile_index])

            for sprite in self._sprites:
                sprite.draw(self._gameDisplay)

            pygame.display.update()

    def getTurn(self):
        self.keepOpen()

        return self._turn

    def P1View(self):
        return self._tiles

    def P2View(self):
        return self._tiles[7:] + self._tiles[:7]

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

    def getScore(self):
        """
        Returns P1 score, P2 score, can be used at any time while game running
        """
        return self._tiles[self.P1_GOAL], self._tiles[self.P2_GOAL]

    def P1Move(self, tile_index):
        """
        Make a move for one of the players (P1).

        Parameters:
        tile_index, [0..5] relative to player view

        Return boolean, True => player chose an empty tile
        """
        assert isinstance(tile_index, int)
        assert tile_index >= 0 and tile_index < 6
        assert self._turn == Turn.P1
        empty = False

        tile_index += 1

        stones = self._tiles[tile_index]
        if stones == 0:
            empty = True
        self._tiles[tile_index] = 0

        i = 0
        place = tile_index
        while stones > 0:
            i += 1
            place = (tile_index + i) % len(self._tiles)

            if place == self.P2_GOAL: # skip enemy goals
                i += 1

            place = (tile_index + i) % len(self._tiles)

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
        return empty

    def P2Move(self, tile_index):
        """
        Make a move for one of the players (P2).

        Parameters:
        tile_index, [0..5] relative to player view

        Return boolean, True => player chose an empty tile
        """
        assert isinstance(tile_index, int)
        assert tile_index >= 0 and tile_index < 6
        assert self._turn == Turn.P2
        empty = False

        tile_index += 8

        stones = self._tiles[tile_index]
        if stones == 0:
            empty = True
        self._tiles[tile_index] = 0

        i = 0
        place = tile_index
        while stones > 0:
            i += 1
            place = (tile_index + i) % len(self._tiles)

            if place == self.P1_GOAL: # skip enemy goals
                i += 1

            place = (tile_index + i) % len(self._tiles)

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
        return empty
