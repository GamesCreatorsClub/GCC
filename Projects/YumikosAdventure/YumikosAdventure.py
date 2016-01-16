import pygame, sys, math, random

import tmx


global screen, screen_size, current_keys, last_keys
global tilemap, playerPos, object, objects, doors, keys


def GameInit():
    global screen, current_keys, screen_size, tilemap, player
    global playerPos, nextPlayerPos, playerCollideRect, nextPlayerCollideRect
    global object, objects
    global doors, keys
    global moved

    moved = False

    screen_size = (640, 640)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    current_keys = pygame.key.get_pressed()

    tilemap = tmx.load('adventure-start.tmx', screen_size)
    objectsLayer = tilemap.layers['objects']
    objects = objectsLayer.objects;
    object = objectsLayer.objects[0]

    player = pygame.image.load("images/player.png")
    # playerPos = pygame.Rect(screen_size[0] / 2 - player.get_width() / 2,
    #                         screen_size[1] / 2 - player.get_height() / 2,
    #                         player.get_width(), player.get_height())

    playerPos = pygame.Rect(200, 240, player.get_width(), player.get_height())
    playerCollideRect = playerPos.move(8, 8)
    playerCollideRect.width = playerCollideRect.width - 16
    playerCollideRect.height = playerCollideRect.height - 16

    nextPlayerPos = playerPos.copy()
    nextPlayerCollideRect = playerCollideRect.copy()

    doors = {}
    keys = {}


def GameReset():
    global map_offset, tilemap
    map_offset = [20, 20]
    tilemap.set_focus(20, 20)

    objectsLayer = tilemap.layers['objects']
    objects = objectsLayer.find("OnCreate")
    for o in objects:
        create = o.properties["OnCreate"]
        exec(create)

    groundLayer = tilemap.layers['ground']

    tiles = groundLayer.find("OnCreate")
    for t in tiles:
        create = t.properties["OnCreate"]
        exec(create)


def UpdateGameScreen(elapsed_ms):
    global map_offset, tilemap
    global playerPos, nextPlayerPos, playerCollideRect, nextPlayerCollideRect
    global moved

    objectsLayer = tilemap.layers['objects']
    groundLayer = tilemap.layers['ground']

    speed = elapsed_ms / 2

    nextPlayerPos[0] = playerPos[0]
    nextPlayerPos[1] = playerPos[1]
    nextPlayerCollideRect[0] = playerCollideRect[0]
    nextPlayerCollideRect[1] = playerCollideRect[1]

    moved = False;
    if current_keys[pygame.K_LEFT] and map_offset[0] > 0:
        nextPlayerPos[0] -= speed
        nextPlayerCollideRect[0] -= speed
        moved = True
    elif current_keys[pygame.K_RIGHT]:
        nextPlayerPos[0] += speed
        nextPlayerCollideRect[0] += speed
        moved = True

    if moved:
        collisionCells = groundLayer.get_in_region(nextPlayerPos.left, nextPlayerPos.top, nextPlayerPos.right, nextPlayerPos.bottom)

        moved = processTilesCollision(collisionCells, nextPlayerCollideRect)

        if moved:
            moved = processObjectCollision(objects, objectsLayer)

        if moved:
            playerPos[0] = nextPlayerPos[0]
            playerCollideRect[0] = nextPlayerCollideRect[0]
        else:
            nextPlayerPos[0] = playerPos[0]
            nextPlayerCollideRect[0] = playerCollideRect[0]

    moved = False
    if current_keys[pygame.K_UP] and map_offset[1] > 0:
        nextPlayerPos[1] -= speed
        nextPlayerCollideRect[1] -= speed
        moved = True
    elif current_keys[pygame.K_DOWN]:
        nextPlayerPos[1] += speed
        nextPlayerCollideRect[1] += speed
        moved = True

    if moved:
        collisionCells = groundLayer.get_in_region(nextPlayerPos.left, nextPlayerPos.top, nextPlayerPos.right, nextPlayerPos.bottom)

        moved = processTilesCollision(collisionCells, nextPlayerCollideRect)

        if moved:
            moved = processObjectCollision(objects, objectsLayer)

        if moved:
            playerPos[1] = nextPlayerPos[1]
            playerCollideRect[1] = nextPlayerCollideRect[1]
        else:
            nextPlayerPos[1] = playerPos[1]
            nextPlayerCollideRect[1] = playerCollideRect[1]

    tilemap.set_focus(playerPos[0], playerPos[1])
    tilemap.update(elapsed_ms)


def processObjectCollision(objects, objectsLayer):
    global collidedObject, moved
    objects = objectsLayer.collide(nextPlayerCollideRect, "OnCollision")
    oi = 0
    oiLen = len(objects)
    while moved and oi < oiLen:
        collidedObject = objects[oi]
        collision = collidedObject.properties["OnCollision"]
        exec(collision)
        oi = oi + 1

    return moved


def processTilesCollision(collisionCells, nextPlayerCollideRect):
    global collidedTile, collidedCell, moved

    if len(collisionCells) > 0:
        cc = 0
        ccLen = len(collisionCells)
        while moved and cc < ccLen:
            collidedCell = collisionCells[cc]
            collidedTile = collidedCell.tile
            collisionRects = collidedTile.collisionRects;
            cr = 0
            crLen = len(collisionRects)
            while moved and cr < crLen:
                if collideWithOffset(nextPlayerCollideRect, collidedCell.px, collidedCell.py, collisionRects[cr]):
                    if "OnCollision" in collidedTile.properties:
                        exec(collidedTile.properties["OnCollision"])
                    else:
                        moved = False
                cr = cr + 1

            cc = cc + 1

    return moved


def collideWithOffset(r1, x, y, r2):
    return r1.x < r2.x + x + r2.w and r1.y < r2.y + y + r2.h and r1.x + r1.w > r2.x + x and r1.y + r1.h > r2.y + y


def PreventMove():
    global moved
    moved = False


def DrawGameScreen():
    global screen, tilemap, player, playerPos
    tilemap.draw(screen)

    nextPlayerPos.move_ip(-tilemap.viewport.x, -tilemap.viewport.y)

    screen.blit(player, nextPlayerPos)


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


GameInit()
GameReset()
while True:
    GameLoop()
