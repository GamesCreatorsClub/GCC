import pygame, sys, math, random

import tmx

# == (1) Create 'global' variables ==
# These are variables that every part of your
# code can 'see' and change
global screen, screen_size, current_keys, last_keys
global tilemap, playerPos, object, objects

# == (2) Define the functions for each task first ==

# == GameInit ==
# Put one time initialisation stuff here 
# it is called just *once*
# at the beginning of our program
def GameInit():
    global screen, current_keys, screen_size, tilemap, player, playerPos, object, objects

    screen_size = (640, 480)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    current_keys = pygame.key.get_pressed()

    tilemap = tmx.load('adventure-start.tmx', screen_size)
    objectsLayer = tilemap.layers['objects']
    objects = objectsLayer.objects;
    object = objectsLayer.objects[0]

    player = pygame.image.load("images/player.png")
    playerPos = pygame.Rect(screen_size[0] / 2 - player.get_width() / 2, screen_size[1] / 2 - player.get_height() / 2,
                            player.get_width(), player.get_height())

# == GameReset ==
# Put 'new game' starting values here.
# This is called many times while the program 
# running whenever a new game is started
def GameReset():
    global map_offset, tilemap
    map_offset = [20, 20]
    tilemap.set_focus(20, 20)

# == UpdateGameScreen ==
# This function is called once every game loop
# to update the main game screen data objects
# Here is where we will put the keyboard responses, 
# collision detection and other game logic.
def UpdateGameScreen(elapsed_ms):
    global map_offset, tilemap, playerPos

    # Make a copy of the current position
    # Move it according to the pressed keys
    # Check the new centre location against the collision
    # map
    # If no collision, then update map position
    if current_keys[pygame.K_UP] and map_offset[1] > 0:
        #map_offset[1] -= elapsed_ms
        playerPos[1] -= elapsed_ms

    if current_keys[pygame.K_DOWN]:
        # map_offset[1] += elapsed_ms
        playerPos[1] += elapsed_ms

    if current_keys[pygame.K_LEFT] and map_offset[0] > 0:
        # map_offset[0] -= elapsed_ms
        playerPos[0] -= elapsed_ms

    if current_keys[pygame.K_RIGHT]:
        # map_offset[0] += elapsed_ms
        playerPos[0] += elapsed_ms

    # tilemap.set_focus(map_offset[0], map_offset[1])
    tilemap.set_focus(playerPos[0], playerPos[1])
    tilemap.update(elapsed_ms)

# == DrawGameScreen ==
# This function is called once every game loop
# to draw the main game screen.
# Here is where we will draw a background, 
# sprites and on screen text.    
def DrawGameScreen():
    global screen, tilemap, player, playerPos
    tilemap.draw(screen)
    pos = playerPos.move(-tilemap.viewport.x, -tilemap.viewport.y)
    screen.blit(player, pos)

# == GameLoop ==
# Put things that have to occur repeatedly
# here. It is called every frame
def GameLoop():
    global current_keys, last_keys, tilemap, playerPos, object, objects
    elapsed_ms = pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    last_keys = current_keys
    current_keys = pygame.key.get_pressed()

    screen.fill((0,0,0))

    UpdateGameScreen(elapsed_ms)
    DrawGameScreen()
    
    # flip the screen to show our drawing
    pygame.display.flip()

    pos = playerPos.move(tilemap.viewport.x, tilemap.viewport.y)

    groundLayer = tilemap.layers['ground']

    collisionCells = groundLayer.get_in_region(pos.left, pos.top, pos.right, pos.bottom)

    if len(collisionCells) > 0:
        for cell in collisionCells:
            tile = cell.tile
            print(", " + str(tile.gid), end="")
        print("")

        colRects = collisionCells[0].tile.collisionRects
        if len(colRects) > 0:
            rect = colRects[0]
            print("Got rect[" + str(rect.left) + ", " + str(rect.top) + "," + str(rect.width) + "," + str(rect.height) + "]")

    for cell in collisionCells:
        tile = cell.tile
        i = pos.collidelist(tile.collisionRects)
        if i >= 0:
            print("found collision " + str(i))

    # for tile in collisionTiles:
    #     if tile

    objectsLayer = tilemap.layers['objects']


    objects = objectsLayer.collide(pos, "OnCollision")

    # print("x=" + str(pos[0]) + ", y=" + str(pos[1]) + " o# " + str(len(objects)))

    for object in objects:
        onCollision = object.properties["OnCollision"]
        exec(onCollision)

# == (3) Call the functions to run the game == 
# We have only *defined* our functions above.
# Here we actually call them to make them happen
GameInit()
GameReset()
while True:
    GameLoop()
