import math

from typing import Union, Optional, ChainMap, Sized, Mapping, Iterator

import time
from pygame.font import Font

import pygame
from engine.level import Level
from engine.tmx import TiledObject
from game.rpg_game_context import RPGGameContext
from game.top_down_game_context import TopDownGameContext
from pygame import Surface, Color, Rect

from engine.game_context import in_context, GameContext

COLOUR_WHITE = pygame.Color("white")
COLOUR_BLACK = pygame.Color("black")
COLOUR_BROWN = pygame.Color("burlywood4")
COLOUR_BROWN_TRANSPARENT = pygame.Color(COLOUR_BROWN.r, COLOUR_BROWN.g, COLOUR_BROWN.b, 128)


def sgn(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    d = a - b
    return -1 if d < 0 else (1 if d > 0 else 0)


class YumikoGame(RPGGameContext):
    def __init__(self, levels: dict[Union[str, int], Level], font: Font, small_font: Font) -> None:
        super().__init__(levels, font, small_font)

    def after_map(self, screen: Surface) -> None:
        self.text_area.draw(screen)
        box_size = self._inventory.image_size
        rect = Rect(screen.get_rect().right - box_size[0] - 2, 50, box_size[0], box_size[1] * 10)
        self._inventory.draw(screen, rect)
