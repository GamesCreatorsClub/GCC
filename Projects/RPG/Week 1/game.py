import pygame, sys, tools, random
from pygame.locals import*

pygame.init()

# Screen size constants
base_tile_size = 16
world_scale = 1
image_scale = 4
tile_size = base_tile_size * image_scale

screen_width = 16 * world_scale * tile_size
screen_height = 9 * world_scale * tile_size

screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()

# Tilesheets and other images

tile_sheet = pygame.image.load("images/tilemap_packed.png").convert_alpha()
tiles = tools.create_scaled_tile_sheet(tile_sheet, 16, image_scale)

player_image = pygame.image.load("images/tile_0085.png").convert_alpha()

player = {
    "image": tools.scale_image(player_image, base_tile_size, image_scale)
    }

level01 = [
    "###",
    "# #",
    "###"
    ]

level_width = len(level01[0])
level_height = len(level01)

background = pygame.Surface((screen_width, screen_height))

fps = 60
clock = pygame.time.Clock()

# Game Loop
game_running = True
while game_running:
    clock.tick()
    dt = clock.get_time() / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Player input
    keys = pygame.key.get_pressed()

    # Drawing to the screen
    screen.blit(background, (0, 0))
    
    pygame.display.update()
    
pygame.quit()
