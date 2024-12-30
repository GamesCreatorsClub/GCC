from typing import Union

from pygame.font import Font

import pygame
from engine.level import Level
from engine.tmx import TiledObject
from game.rpg_game_context import RPGGameContext
from pygame import Surface, Rect

from engine.game_context import in_context

COLOUR_WHITE = pygame.Color("white")
COLOUR_BLACK = pygame.Color("black")
COLOUR_BROWN = pygame.Color("burlywood4")
COLOUR_BROWN_TRANSPARENT = pygame.Color(COLOUR_BROWN.r, COLOUR_BROWN.g, COLOUR_BROWN.b, 128)


def sgn(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    d = a - b
    return -1 if d < 0 else (1 if d > 0 else 0)


class YumikoGameContext(RPGGameContext):
    def __init__(self, levels: dict[Union[str, int], Level], font: Font, small_font: Font) -> None:
        super().__init__(levels, font, small_font)

    def after_map(self, screen: Surface) -> None:
        self.text_area.draw(screen)
        box_size = self._inventory.image_size
        rect = Rect(screen.get_rect().right - box_size[0] - 2, 50, box_size[0], box_size[1] * 10)
        self._inventory.draw(screen, rect)

    @in_context
    def record_position(self, obj: TiledObject) -> None:
        obj.properties["startx"] = obj.x
        obj.properties["starty"] = obj.y
