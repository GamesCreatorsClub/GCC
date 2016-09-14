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
"              o                 ",
"                                ",
"                                ",
"                                ",
"                                ",
"          #########             ",
"                                ",
"                                ",
"                                ",
"              x                 ",
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

level8 = [
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

level9 = [
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

level10 = [
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

level11 = [
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

level12 = [
"                                ",
"     #######################    ",
"     #               #     #    ",
"     # ############# # ### #    ",
"     # #           # ##### #    ",
"     # # ######### #       #    ",
"     # #         # # #######    ",
"     # ######### # #     x #    ",
"     #           #o#########    ",
"     # ######### # # #     #    ",
"     # #         # # # ### #    ",
"     # #  ######## # # # # #    ",
"     # #           # # # # #    ",
"     # ############# # # # #    ",
"     #                 #   #    ",
"     #######################    ",
]

levels = [level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12]
level = 11

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
speed_up = 1
keys = []
return_pressed = False
score = 0
moves = 0
automatic = False
breadcrumbs = []
keys = []

def init(updatePlayer):
    global wall_sprite, CELL_WIDTH, CELL_HEIGHT, screen
    global game_state, level_exit, player, update_player
    global keys, screen_rect
    global left_bc, right_bc, up_bc, down_bc

    update_player = updatePlayer

    pygame.init()
    wall_sprite = pygame.image.load("wall_32.png")
    left_bc = pygame.image.load("left-bc.png")
    right_bc = pygame.image.load("right-bc.png")
    up_bc = pygame.image.load("up-bc.png")
    down_bc = pygame.image.load("down-bc.png")

    CELL_WIDTH = wall_sprite.get_width()
    CELL_HEIGHT = wall_sprite.get_height()

    selectedLevel = levels[level]

    # Global Game Data
    screen = pygame.display.set_mode((len(selectedLevel[0]) * CELL_WIDTH, len(selectedLevel) * CELL_HEIGHT))

    screen_rect = pygame.Rect(-1, -1, screen.get_width(), screen.get_height())

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
        "speed":32,
        }


    initFonts()
    createMap(selectedLevel, player, level_exit)


def exitPos():
    global level_exit, CELL_WIDTH, CELL_HEIGHT
    return pygame.Rect(level_exit["rect"].x / CELL_WIDTH, level_exit["rect"].y / CELL_HEIGHT, 1, 1)

def playerPos():
    global player, CELL_WIDTH, CELL_HEIGHT
    return pygame.Rect(player["rect"].x / CELL_WIDTH, player["rect"].y / CELL_HEIGHT, 1, 1)

def map(direction):
    global levels, level

    player_pos = playerPos().move(direction)

    if player_pos.x < 0 or player_pos.y < 0:
        return False

    map = levels[level]
    if player_pos.y < len(map):
        line = map[player_pos.y]

        if player_pos.x < len(line):
            return line[player_pos.x] != '#'

    return False

def mapAt(x, y):
    global levels, level

    map = levels[level]
    line = map[y]

    return line[x] != '#'

def addBreadcrumb(direction):
    player_pos = playerPos()
    addBreadcrumbAt(direction, player_pos.x, player_pos.y)

def addBreadcrumbAt(direction, x, y):
    breadcrumbs.append([x, y, direction, direction])

def goBack():
    entry = lastBreadcrumb()
    if entry == None:
        return None

    player_pos = playerPos()
    if entry[0] == player_pos.x and entry[1] == player_pos.y:
        removeBreadcrumb();
        entry = lastBreadcrumb()
        if entry == None:
            return None

    if entry[0] < player_pos.x:
        return Left
    if entry[0] > player_pos.x:
        return Right
    if entry[1] < player_pos.y:
        return Up
    if entry[1] < player_pos.y:
        return Right

    return None

def removeBreadcrumb():
    del breadcrumbs[len(breadcrumbs) - 1]


def hasVisited(direction):
    player_pos = playerPos().move(direction)

    return hasVisitedAt(player_pos.x, player_pos.y)

def hasVisitedAt(x, y):
    return breadCrumbFor(x, y) != None

def lastBreadcrumb():
    if len(breadcrumbs) > 0:
        entry = breadcrumbs[len(breadcrumbs) - 1]
        return entry

    return None

def currentBreadcrumb():
    player_pos = playerPos()
    return breadCrumbFor(player_pos.x, player_pos.y)

def breadCrumbFor(x, y):
    i = 0
    while i < len(breadcrumbs):
        entry = breadcrumbs[i]
        if entry[0] == x and entry[1] == y:
            return entry
        i = i + 1
    return None


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
    global left_bc, right_bc, up_bc, down_bc
    global CELL_WIDTH, CELL_HEIGHT, breadcrumbs

    breadcrumb_rect = pygame.Rect(0, 0, 0, 0)

    # -- Draw the screen --
    # Background
    clearScreen("RoyalBlue")

    # Walls
    for wall in walls:
        # shadow first...
        pygame.draw.rect(screen, (50, 50, 170), wall.move(10, 10))

    for breadcrumb in breadcrumbs:
        breadcrumb_rect.move_ip(-breadcrumb_rect.x, -breadcrumb_rect.y)
        breadcrumb_rect.move_ip(breadcrumb[0] * CELL_WIDTH, breadcrumb[1] * CELL_HEIGHT)
        if breadcrumb[2][0] == -1:
            screen.blit(left_bc, breadcrumb_rect)
        elif breadcrumb[2][0] == 1:
            screen.blit(right_bc, breadcrumb_rect)
        elif breadcrumb[2][1] == -1:
            screen.blit(up_bc, breadcrumb_rect)
        else:
            screen.blit(down_bc, breadcrumb_rect)

    # Draw Stuff...
    drawPlayer(player)

    for wall in walls:
        # now the walls
        screen.blit(wall_sprite, wall)

    # Exit
    screen.blit(level_exit['image'], level_exit['rect'])

STATE_MAIN = 0
STATE_MOVE = 1
STATE_MOVING = 2
STATE_WIN = 3
STATE_LOSE = 4


def mainLoop():
    global player, game_state, level_exit, levels, level, speed_up
    global CELL_WIDTH, CELL_HEIGHT, screen_rect, keys, score, moves
    global automatic, keys
    global STATE_MAIN, STATE_MOVE, STATE_MOVING, STATE_WIN, STATE_LOSE

    cheating = False

    # === Main Game Loop ===
    while True:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        player_rect = player["rect"]

        if game_state == STATE_MAIN:
            automatic = False
            if keys[pygame.K_SPACE]:
                automatic = False
                # direction = update_player()
                game_state = STATE_MOVE
            elif keys[pygame.K_RETURN]:
                automatic = True
                # direction = update_player()
                game_state = STATE_MOVE
            else:
                drawScreen()


        if game_state == STATE_MOVE:
            #moves = moves + 1
            if moves > 1024:
                game_state = STATE_LOSE
            else:
                direction = update_player()
                game_state = STATE_MOVING
                if direction == None:
                    game_state = STATE_MOVE
                else:
                    step = direction[0] + direction[1]
                    if step != 1 and step != -1:
                        cheating = True
                        game_state = STATE_LOSE
                    else:
                        game_state = STATE_MOVING
                        player_pos = playerPos()
                        if hasVisitedAt(player_pos.x, player_pos.y):
                            entry = breadCrumbFor(player_pos.x, player_pos.y)
                            entry[2]  = direction
                        # else:
                        #     addBreadcrumb(direction)


        if game_state == STATE_MOVING:
            player_rect = player_rect.move((direction[0] * player["speed"], direction[1] * player["speed"]))
            # for i in range(0, player["speed"] * speed_up):
            player["rect"] = player_rect
            drawScreen()

            if player_rect.x % CELL_WIDTH == 0 and player_rect.y % CELL_HEIGHT == 0:
                if player_rect.colliderect(level_exit['rect']):
                    player["rect"] = player_rect

                    level = level + 1
                    deduct = int(moves / 10) -1
                    if deduct < 0:
                        deduct = 0
                    score = score + 100 - deduct
                    moves = 0
                    game_state = STATE_WIN

                elif not player_rect.colliderect(screen_rect):
                    game_state = STATE_LOSE
                elif player_rect.collidelist(walls) != -1:
                    player_rect = player["rect"]
                    drawScreen()
                else:

                    if not automatic:
                        game_state = STATE_MAIN
                    else:
                        game_state = STATE_MOVE

        if game_state == STATE_WIN:
            breadcrumbs.clear()
            clearScreen("DarkOliveGreen")
            if level >= len(levels):
                drawLargeText("Congratulations! You made tt!", (260, 200), "Green")
            else:
                drawLargeText("You made through the level!", (260, 200), "Green")
                drawLargeText("Press Enter for the next level", (260, 240), "Green")
                createMap(levels[level], player, level_exit)
                checkForResetGame(player)


        if game_state == STATE_LOSE:
            breadcrumbs.clear()
            level = 0
            moves = 0
            automatic = False
            clearScreen("FireBrick")
            drawLargeText("Oh No - You Lose!", (350, 220), "Red")
            if cheating:
                drawLargeText("Were you cheating?", (350, 240), "Red")
            checkForResetGame(player)

        drawLargeText("Score: " + str(score), (11, 21), "Black")
        drawLargeText("Score: " + str(score), (10, 20), "White")
        pygame.display.flip()
        # End of the game loop


