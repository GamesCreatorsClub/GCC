import pygame, sys, random

level1 = [
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"              o                x",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
]

level2 = [
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"x             o                 ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
]

level3 = [
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"              o                 ",
"                                ",
"                             x  ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
]

level4 = [
"                                ",
"                                ",
"                                ",
"    x                           ",
"                                ",
"                                ",
"                                ",
"              o                 ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
]

level5 = [
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"              #                 ",
"              #                 ",
"    o         #            x    ",
"              #                 ",
"              #                 ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
]

level6 = [
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"              ######            ",
"                   #       x    ",
"    o              #            ",
"                   #            ",
"                   #            ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
]

level7 = [
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
" ###################            ",
"                   #       x    ",
"    o              #            ",
"                   #            ",
"                   #            ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
"                                ",
]

level8 = [
"                                ",
"                                ",
"                                ",
"       #############            ",
"                   #            ",
"                   #            ",
"                   #       x    ",
"    o              #            ",
"                   #            ",
"                   #            ",
"                   #            ",
"                   #            ",
"       #############            ",
"                                ",
"                                ",
"                                ",
]

level9 = [
"                                ",
"                                ",
"                                ",
"       #############            ",
"                   #            ",
"                   #            ",
"                   #       x    ",
"                o  #            ",
"                   #            ",
"                   #            ",
"                   #            ",
"                   #            ",
"       #############            ",
"                                ",
"                                ",
"                                ",
]

level10 = [
"                                ",
"                                ",
"       #############            ",
"       #           #            ",
"       # ######### #            ",
"       #         # #            ",
"       ######### # #       x    ",
"                 #o#            ",
"       ######### # #            ",
"       #         # #            ",
"       #  ######## #            ",
"       #           #            ",
"       #############            ",
"                                ",
"                                ",
"                                ",
]

levels = [level1, level2, level3, level4, level5, level6, level7, level8, level9, level10]
level = 0

Left = [-1, 0]
Right = [1, 0]
Up = [0, -1]
Down = [0, 1]

walls = []
screen_rect = None
player = None
level_exit = None
update_player = None
CELL_WIDTH = 0
CELL_HEIGHT = 0
keys = []
return_pressed = False

def init(updatePlayer):
    global wall_sprite, CELL_WIDTH, CELL_HEIGHT, screen
    global game_state, level_exit, player, update_player
    global keys, screen_rect

    update_player = updatePlayer

    pygame.init()
    wall_sprite = pygame.image.load("wall_32.png")

    CELL_WIDTH = wall_sprite.get_width()
    CELL_HEIGHT = wall_sprite.get_height()

    # Global Game Data
    screen = pygame.display.set_mode((len(level1[0]) * CELL_WIDTH, len(level1) * CELL_HEIGHT))

    screen_rect = pygame.Rect(CELL_WIDTH - 1, CELL_HEIGHT - 1, screen.get_width() - CELL_WIDTH + 1, screen.get_height() - CELL_HEIGHT + 1)

    keys = []
    game_state = 0;

    level_exit = {
        "image":pygame.image.load("exit_32.png"),
        "rect":pygame.Rect(0, 0, 32, 32)
        }

    player = {
        "image": pygame.image.load("player_down_0.png"),
        "rect":pygame.Rect(0, 0, 32, 32),
        "start_rect":pygame.Rect(0, 0, 32, 32),
        "speed":4,
        }


    initFonts()
    createMap(level1, player, level_exit)


def exit():
    global level_exit
    return [level_exit[0] / CELL_WIDTH, level_exit[1] / CELL_HEIGHT]

def drawPlayer(player):
    screen.blit(player['image'], player['rect'])


# Helper Functions
def initFonts():
    global g_large_font, g_small_font
    g_large_font = pygame.font.SysFont("jokerman", 50)
    g_small_font = pygame.font.SysFont("jokerman", 18)

def drawLargeText(text, position, colour):
    font_colour = pygame.Color(colour)
    rendered_text = g_large_font.render(text, 1, font_colour)
    shadow_text = g_large_font.render(text, 1, (0, 0, 0))
    screen.blit(shadow_text, (position[0] + 5, position [1] + 5))
    screen.blit(rendered_text, position)

def drawSmallText(text, position, colour):
    font_colour = pygame.Color(colour)
    rendered_text = g_small_font.render(text, 1, font_colour)
    screen.blit(rendered_text, position)

def clearScreen(colour):
    clear_colour = pygame.Color(colour)
    screen.fill(clear_colour)

def checkForResetGame(player):
    global game_state, keys, return_pressed

    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        return_pressed = True
    elif return_pressed:
        return_pressed = False
        game_state = 0
        player["rect"] = player["start_rect"]


def createMap(level, player, level_exit):
    global screen, walls, enemies
    block_size = 32
    
    # Reset the wall & enemy lists
    walls[:] = []

    # Fill the walls array with rectangles for each '#'
    x = y = 0
    for row in level:
        for col in row:
            if col == " ":
                x += block_size
                continue
            
            elif col == "#":
                walls.append(pygame.Rect(x, y, block_size, block_size))

            # Set the player position if we find an 'o'
            elif col == "o":
                player["rect"] = pygame.Rect(x, y, block_size, block_size)
                player["start_rect"] = pygame.Rect(x, y, block_size, block_size)

            # Set the exit position if we find an 'x'
            elif col == "x":
                level_exit["rect"] = pygame.Rect(x, y, block_size, block_size)

            x += block_size
        y += block_size
        x = 0

def drawScreen():
    global player, game_state, level_exit

    # -- Draw the screen --
    # Background
    clearScreen("RoyalBlue")

    # Walls
    for wall in walls:
        # shadow first...
        pygame.draw.rect(screen, (50, 50, 170), wall.move(10, 10))

    # Draw Stuff...
    drawPlayer(player)

    for wall in walls:
        # now the walls
        screen.blit(wall_sprite, wall)

    # Exit
    screen.blit(level_exit['image'], level_exit['rect'])


def mainLoop():
    global player, game_state, level_exit, levels, level
    global CELL_WIDTH, CELL_HEIGHT, screen_rect, keys

    # === Main Game Loop ===
    while True:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if game_state == 0:
            player_rect = player["rect"]
            # Check if we have reached the exit or hit enemy
            if player_rect.colliderect(level_exit['rect']):
                level = level + 1
                game_state = 1
            elif not player_rect.colliderect(screen_rect):
                game_state = 2
            else:
                drawScreen()
                if keys[pygame.K_SPACE]:
                    game_state = 3
                    direction = update_player()
                elif keys[pygame.K_RETURN]:
                    game_state = 4
                    direction = update_player()
                elif keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
        elif game_state == 1:
            clearScreen("DarkOliveGreen")
            if level >= len(levels):
                drawLargeText("Congratulations! You Made It!", (100, 100), "Green")
            else:
                drawLargeText("You Made Through Level!", (110, 100), "Green")
                drawLargeText("Press Enter for next level", (110, 140), "Green")
                createMap(levels[level], player, level_exit)
                checkForResetGame(player)

        elif game_state == 2:
            level = 0
            clearScreen("FireBrick")
            drawLargeText("Oh No - You Lose!", (90, 100), "Red")
            checkForResetGame(player)

        elif game_state == 3:
            player_rect = player["rect"]
            for i in range(0, player["speed"]):
                player_rect = player_rect.move(direction)
            player["rect"] = player_rect
            if player_rect.x % CELL_WIDTH == 0 and player_rect.y % CELL_HEIGHT == 0:
                game_state = 0
            else:
                drawScreen()

        elif game_state == 4:
            player_rect = player["rect"]
            for i in range(0, player["speed"] * 4):
                player_rect = player_rect.move(direction)
            player["rect"] = player_rect
            if player_rect.x % CELL_WIDTH == 0 and player_rect.y % CELL_HEIGHT == 0:
                if player_rect.colliderect(level_exit['rect']):
                    level = level + 1
                    game_state = 1
                elif not player_rect.colliderect(screen_rect):
                    game_state = 2
                else:
                    direction = update_player()
            else:
                drawScreen()

        pygame.display.flip()
        # End of the game loop


