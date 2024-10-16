import pygame
from pygame import Rect

from engine.game import Game
from engine.level import Level

from engine.debug import (Debug)
from game.top_down_game_context import TopDownGameContext

screen_size = (1024, 640)

pygame.init()
pygame.font.init()


screen = pygame.display.set_mode(screen_size)
screen_rect = screen.get_rect()

levels = Level.load_levels(screen_rect, "assets/start.tmx")
game_context = TopDownGameContext(levels)
game_context.set_level(levels["start"])

game = Game(screen, game_context, 60, True)

game.main_loop()

pygame.display.quit()
pygame.quit()
