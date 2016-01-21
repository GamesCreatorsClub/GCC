import pygame, tmx, sys

def Init(screen_size, game_pointer):
    global screen, current_keys, player
    global mouse_click_pos, mouse_is_down

    global playerPos, nextPlayerPos, playerCollideRect, nextPlayerCollideRect
    global moved, game

    game = game_pointer

    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    current_keys = pygame.key.get_pressed()
    mouse_is_down = False

    moved = False

    player = pygame.image.load("images/player.png")
    # playerPos = pygame.Rect(200, 240, player.get_width(), player.get_height())
    # playerCollideRect = playerPos.move(8, 16)
    # playerCollideRect.width = playerCollideRect.width - 16
    # playerCollideRect.height = playerCollideRect.height - 16
    #
    # nextPlayerPos = playerPos.copy()
    # nextPlayerCollideRect = playerCollideRect.copy()

    mouse_click_pos = [-1, -1]

def setupPlayer(playerPosition):
    global player, playerPos, nextPlayerPos, playerCollideRect, nextPlayerCollideRect

    playerPos = pygame.Rect(playerPosition[0], playerPosition[1], player.get_width(), player.get_height())
    playerCollideRect = playerPos.move(8, 16)
    playerCollideRect.width = playerCollideRect.width - 16
    playerCollideRect.height = playerCollideRect.height - 16

    nextPlayerPos = playerPos.copy()
    nextPlayerCollideRect = playerCollideRect.copy()


def Reset():
    return None

def LoadMap(mapName):
    global tilemap, playerPos

    tilemap = tmx.load(mapName, screen.get_size())

    objectLayer = tilemap.layers["objects"]
    startObject = objectLayer.find_by_name("start_position")
    if not startObject == None:
        objectLayer.objects.remove(startObject)
        setupPlayer((startObject.px, startObject.py))
    else:
        setupPlayer((tilemap.px_width / 2, tilemap.px_height / 2))

    tilemap.set_focus(playerPos.x, playerPos.y)

    if "OnCreate" in tilemap.properties:
        onCreate = tilemap.properties["OnCreate"]
        game.execute(onCreate)

    processOnCreate(tilemap.layers["objects"])
    processOnCreate(tilemap.layers["ground1"])
    processOnCreate(tilemap.layers["ground2"])
    processOnCreate(tilemap.layers["overlay"])


def processOnCreate(layer):
    tiles = layer.find("OnCreate")
    for t in tiles:
        onCreate = t.properties["OnCreate"]
        game.execute(onCreate)


def processObjectClick(object):
    global clickedObject, moved

    clickedObject = object

    if clickedObject != None and "OnClick" in clickedObject.properties:
        onClick = clickedObject.properties["OnClick"]
        game.execute(onClick)

    return moved


def processObjectCollision(objectsLayer):
    global moved

    objects = objectsLayer.collide2(nextPlayerCollideRect, "OnCollision", "OnCollisionStart")
    oi = 0
    oiLen = len(objects)
    collided = False
    while not collided and moved and oi < oiLen: # Processing only first object that collided!
        collidedObject = objects[oi]
        if "tile" in collidedObject and "collisionRects" in collidedObject.tile and len(collidedObject.tile.collisionRects) > 0:
            collisionRects = collidedObject.tile.collisionRects;
            cr = 0
            crLen = len(collisionRects)
            while not collided and cr < crLen:
                if collideWithOffset(nextPlayerCollideRect, collidedObject.px, collidedObject.py, collisionRects[cr]):
                    collided = True
                cr = cr + 1
        else:
            collided = True

        if collided:
            if game.collidedObject != None and game.collidedObject != collidedObject:
                processObjectsOnMethod(game.collidedObject, "OnCollisionEnd")

            if game.collidedObject != collidedObject:
                game.collidedObject = collidedObject
                if "tile" in collidedObject:
                    game.collidedTile = collidedObject.tile
                processObjectsOnMethod(collidedObject, "OnCollisionStart")

            processObjectsOnMethod(collidedObject, "OnCollision")

        oi = oi + 1

    if not collided:
        if game.collidedObject != None:
            processObjectsOnMethod(game.collidedObject, "OnCollisionEnd")
            game.collidedObject = None

    return moved

def processObjectsOnMethod(collidedObject, methodName):
    global moved

    collision = None
    if methodName in collidedObject.properties:
        collision = collidedObject.properties[methodName]
    elif methodName in collidedObject:
        collision = collidedObject[methodName]
    if collision != None:
        game.execute(collision)


def processTilesCollision(collisionCells, nextPlayerCollideRect):
    global moved

    if len(collisionCells) > 0:
        cc = 0
        ccLen = len(collisionCells)
        while moved and cc < ccLen:
            collidedCell = collisionCells[cc]
            collidedTile = collidedCell.tile

            game.collidedCell = collisionCells
            game.collidedTile = collidedTile

            collisionRects = collidedTile.collisionRects;
            cr = 0
            crLen = len(collisionRects)
            while moved and cr < crLen:
                if collideWithOffset(nextPlayerCollideRect, collidedCell.px, collidedCell.py, collisionRects[cr]):
                    if "OnCollision" in collidedTile.properties:
                        game.execute(collidedTile.properties["OnCollision"])
                    else:
                        moved = False
                cr = cr + 1

            cc = cc + 1

    return moved


def collideWithOffset(r1, x, y, r2):
    return r1.x < r2.x + x + r2.w and r1.y < r2.y + y + r2.h and r1.x + r1.w > r2.x + x and r1.y + r1.h > r2.y + y


def MovePlayer(elapsed_ms):
    global tilemap
    global player, playerPos, nextPlayerPos, playerCollideRect, nextPlayerCollideRect
    global moved, mouse_is_down, mouse_click_pos

    objectsLayer = tilemap.layers["objects"]
    ground1Layer = tilemap.layers["ground1"]
    ground2Layer = tilemap.layers["ground2"]

    speed = elapsed_ms / 4

    nextPlayerPos[0] = playerPos[0]
    nextPlayerPos[1] = playerPos[1]
    nextPlayerCollideRect[0] = playerCollideRect[0]
    nextPlayerCollideRect[1] = playerCollideRect[1]

    move_by_mouse = mouse_is_down
    moved = False;

    if current_keys[pygame.K_LEFT] and playerPos[0] > 0:
        nextPlayerPos[0] -= speed
        nextPlayerCollideRect[0] -= speed
        moved = True
    elif current_keys[pygame.K_RIGHT] and playerPos[0] < tilemap.px_width - player.get_width():
        nextPlayerPos[0] += speed
        nextPlayerCollideRect[0] += speed
        moved = True

    if not moved and move_by_mouse:
        if playerPos[0] - mouse_click_pos[0] - tilemap.viewport.x >= speed:
            nextPlayerPos[0] -= speed
            nextPlayerCollideRect[0] -= speed
            moved = True
        elif mouse_click_pos[0] + tilemap.viewport.x - playerPos[0] >= speed:
            nextPlayerPos[0] += speed
            nextPlayerCollideRect[0] += speed
            moved = True

        clickedCell = objectsLayer.get_at(mouse_click_pos[0] + tilemap.viewport.x, mouse_click_pos[1] + tilemap.viewport.y)
        moved = processObjectClick(clickedCell)
        if not moved:
            move_by_mouse = False

    if moved:
        collisionCells = ground1Layer.get_in_region(nextPlayerPos.left, nextPlayerPos.top, nextPlayerPos.right, nextPlayerPos.bottom)
        moved = processTilesCollision(collisionCells, nextPlayerCollideRect)

        if moved:
            collisionCells = ground2Layer.get_in_region(nextPlayerPos.left, nextPlayerPos.top, nextPlayerPos.right, nextPlayerPos.bottom)
            moved = processTilesCollision(collisionCells, nextPlayerCollideRect)

        if moved:
            moved = processObjectCollision(objectsLayer)

        if moved:
            playerPos[0] = nextPlayerPos[0]
            playerCollideRect[0] = nextPlayerCollideRect[0]
        else:
            nextPlayerPos[0] = playerPos[0]
            nextPlayerCollideRect[0] = playerCollideRect[0]

    moved = False
    if current_keys[pygame.K_UP] and playerPos[1] > 0:
        nextPlayerPos[1] -= speed
        nextPlayerCollideRect[1] -= speed
        moved = True
    elif current_keys[pygame.K_DOWN] and playerPos[1] < tilemap.px_height - player.get_height():
        nextPlayerPos[1] += speed
        nextPlayerCollideRect[1] += speed
        moved = True

    if not moved and move_by_mouse:
        if playerPos[1] - mouse_click_pos[1] - tilemap.viewport.y >= speed:
            nextPlayerPos[1] -= speed
            nextPlayerCollideRect[1] -= speed
            moved = True
        elif mouse_click_pos[1] + tilemap.viewport.y - playerPos[1] >= speed:
            nextPlayerPos[1] += speed
            nextPlayerCollideRect[1] += speed
            moved = True

    if moved:
        collisionCells = ground1Layer.get_in_region(nextPlayerPos.left, nextPlayerPos.top, nextPlayerPos.right, nextPlayerPos.bottom)
        moved = processTilesCollision(collisionCells, nextPlayerCollideRect)

        if moved:
            collisionCells = ground2Layer.get_in_region(nextPlayerPos.left, nextPlayerPos.top, nextPlayerPos.right, nextPlayerPos.bottom)
            moved = processTilesCollision(collisionCells, nextPlayerCollideRect)

        if moved:
            moved = processObjectCollision(objectsLayer)

        if moved:
            playerPos[1] = nextPlayerPos[1]
            playerCollideRect[1] = nextPlayerCollideRect[1]
        else:
            nextPlayerPos[1] = playerPos[1]
            nextPlayerCollideRect[1] = playerCollideRect[1]

    tilemap.set_focus(playerPos[0], playerPos[1])
    tilemap.update(elapsed_ms)


def ProcessEvents(elapsed_ms):
    global mouse_click_pos, mouse_is_down
    global current_keys, last_keys

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click_pos[0] = event.pos[0]
            mouse_click_pos[1] = event.pos[1]
            mouse_is_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_is_down = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_is_down:
                mouse_click_pos[0] = event.pos[0]
                mouse_click_pos[1] = event.pos[1]

    last_keys = current_keys
    current_keys = pygame.key.get_pressed()


def DrawScreen():
    global screen
    global tilemap
    global nextPlayerPos
    global player

    nextPlayerPos.move_ip(-tilemap.viewport.x, -tilemap.viewport.y)

    screen.fill((0,0,0))

    for layer in tilemap.layers:
        if layer.visible:
            layer.draw(screen)
        if layer.name == "objects":
            screen.blit(player, nextPlayerPos)
