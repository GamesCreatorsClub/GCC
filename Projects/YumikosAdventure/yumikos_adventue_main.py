import pygame

from engine.game import Game
from engine.level import Level

from yumiko_game import YumikoGame

screen_size = (1024, 640)

pygame.init()
pygame.font.init()

small_font = pygame.font.SysFont("apple casual", 16)
font = pygame.font.SysFont("apple casual", 24)

screen = pygame.display.set_mode(screen_size)
screen_rect = screen.get_rect()

levels = Level.load_levels(
    screen_rect,
    "assets/start.tmx",
    "assets/example-map.tmx"
)

game_context = YumikoGame(levels, font, small_font)
game_context.set_level(levels["start"])
game_context.screen_size = screen_size

game = Game(
    screen,
    game_context,
    60, True)

game.before_map = None
game.after_map = game_context.after_map

game.main_loop()

pygame.display.quit()
pygame.quit()
