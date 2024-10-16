import pygame, tmx, sys

MAX_TEXT_LINES = 7
DEFAULT_TEXT_TIMEOUT = 60 * 10
MARGIN_BETWEEN_LINES = 5

lineHeight = 0

LEFT = 1
RIGHT = 2
UP = 4
DOWN = 8

playerPos = []
tilesByName = {}
autoAnimationObjects = []
animationObjects = []

playerInventory = []

textLines = []
textLinesTimeout = []
textLastText = ''

objectsSurface = None
charactersSurface = None
inventorySurface = None

inventoryBox = None
showInventory = True

objectLayer = None

font = None

def Init(screenSize, game_pointer):
    global screen, current_keys, player, objectsSurface, charactersSurface
    global mouse_click_pos, last_mouse_click_pos, mouse_is_down, last_mouse_is_down

    global playerPos, nextPlayerPos, playerCollideRect, nextPlayerCollideRect
    global moved, game
    global tilesByName

    global playerInventory
    global screen_size
    global inventoryBox, inventorySurface
    global font, lineHeight, MARGIN_BETWEEN_LINES

    font = pygame.font.SysFont("apple casual" , 24)
    lineHeight = font.get_height() + MARGIN_BETWEEN_LINES

    game = game_pointer

    pygame.init()

    screen_size = screenSize
    screen = pygame.display.set_mode(screen_size)

    current_keys = pygame.key.get_pressed()
    mouse_is_down = False
    last_mouse_is_down = False

    moved = False

    objectsSurface = pygame.image.load("images/objects.png")
    charactersSurface = pygame.image.load("images/characters.png")
    inventorySurface = pygame.image.load("images/inventory.png")

    player = charactersSurface.subsurface(pygame.Rect(0, 0, 32, 32))
    inventoryBox = inventorySurface.subsurface(pygame.Rect(0, 0, 36, 36))

    mouse_click_pos = [-1, -1]
    last_mouse_click_pos = [-1, -1]
    tilesByName = {}

    font_Small = pygame.font.SysFont("Arial", 12)
    font_Medium = pygame.font.SysFont("Arial", 24)
    font_Large = pygame.font.SysFont("Arial", 48)


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


def teleportToObject(name):
    global objectLayer

    object = objectLayer.find_by_name(name)
    if not object == None:
        setupPlayer((object.px, object.py))
    else:
        setupPlayer((tilemap.px_width / 2, tilemap.px_height / 2))


def LoadMap(mapName):
    global tilemap, playerPos, tilesByName, autoAnimationObjects, animationObjects, objectLayer

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

    processNames()

    processOnCreate(tilemap.layers["objects"])
    processOnCreate(tilemap.layers["ground1"])
    processOnCreate(tilemap.layers["ground2"])
    processOnCreate(tilemap.layers["overlay"])

    autoAnimationObjects = tilemap.layers["objects"].find("Animate")
    animationObjects = tilemap.layers["objects"].find("OnAnimate")


def processNames():
    global tilesByName

    tilesByName = {}

    for tileId in tilemap.tilesets:
        tile = tilemap.tilesets[tileId]
        if "Name" in tile.properties:
            tilesByName[tile.properties["Name"]] = tile
        elif "name" in tile.properties:
            tilesByName[tile.properties["name"]] = tile


def processOnCreate(layer):
    tiles = layer.find("OnCreate")
    for t in tiles:
        onCreate = t.properties["OnCreate"]
        game.createdObject = t
        game.execute(onCreate)


def processObjectClick(object):
    global clickedObject, moved

    clickedObject = object

    if clickedObject != None and "OnClick" in clickedObject.properties:
        onClick = clickedObject.properties["OnClick"]
        game.clickedObject = clickedObject
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


def Animate():

    for object in animationObjects:
        game.animatedObject = object
        processObjectsOnMethod(object, "OnAnimate")

    for object in autoAnimationObjects:
        AnimateObject(object)


def AnimateObject(object):

    if "animation_timeout" in object.properties:
        animationTimeout = object.properties["animation_timeout"]
    else:
        animationTimeout = 1

    if not "AnimationSpeed" in object.properties:
        object.properties["AnimationSpeed"] = "1"
    animationSpeed = int(object.properties["AnimationSpeed"])

    animationTimeout = animationTimeout - 1
    if animationTimeout > 1:
        object.properties["animation_timeout"] = animationTimeout
        return

    object.properties["animation_timeout"] = animationSpeed


    if "current_frame" not in object.properties:
        object.properties["current_frame"] = 1
    currentFrame = object.properties["current_frame"]

    frameName = object.properties["Frame" + str(currentFrame)]

    object.tile = tilesByName[frameName]

    currentFrame = currentFrame + 1
    if not "Frame" + str(currentFrame) in object.properties:
        currentFrame = 1

    object.properties["current_frame"] = currentFrame


def MovePlayerWithKeys(elapsed_ms):
    direction = 0
    if current_keys[pygame.K_LEFT] or current_keys[pygame.K_a]:
        direction = direction + LEFT
    elif current_keys[pygame.K_RIGHT] or current_keys[pygame.K_d]:
        direction = direction + RIGHT
    if current_keys[pygame.K_UP] or current_keys[pygame.K_w]:
        direction = direction + UP
    elif current_keys[pygame.K_DOWN] or current_keys[pygame.K_s]:
        direction = direction + DOWN

    movePlayerInternal(elapsed_ms, direction, mouse_is_down)


def MovePlayer(elapsed_ms, direction):
    movePlayerInternal(elapsed_ms, direction, False)


def movePlayerInternal(elapsed_ms, direction, move_by_mouse):
    global tilemap
    global player, playerPos, nextPlayerPos, playerCollideRect, nextPlayerCollideRect
    global moved, mouse_click_pos

    objectsLayer = tilemap.layers["objects"]
    ground1Layer = tilemap.layers["ground1"]
    ground2Layer = tilemap.layers["ground2"]

    speed = elapsed_ms / 4

    nextPlayerPos[0] = playerPos[0]
    nextPlayerPos[1] = playerPos[1]
    nextPlayerCollideRect[0] = playerCollideRect[0]
    nextPlayerCollideRect[1] = playerCollideRect[1]

    moved = False;

    if direction & LEFT != 0 and playerPos[0] > 0:
        nextPlayerPos[0] -= speed
        nextPlayerCollideRect[0] -= speed
        moved = True
    elif direction & RIGHT != 0 and playerPos[0] < tilemap.px_width - player.get_width():
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
    if direction & UP != 0 and playerPos[1] > 0:
        nextPlayerPos[1] -= speed
        nextPlayerCollideRect[1] -= speed
        moved = True
    elif direction & DOWN != 0 and playerPos[1] < tilemap.px_height - player.get_height():
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


def ProcessClick(elapsed_ms):
    global tilemap
    global player, playerPos, nextPlayerPos, playerCollideRect, nextPlayerCollideRect
    global moved, mouse_is_down, mouse_click_pos

    if mouse_is_down and not last_mouse_is_down:
        objectsLayer = tilemap.layers["objects"]
        clickedCell = objectsLayer.get_at(mouse_click_pos[0] + tilemap.viewport.x, mouse_click_pos[1] + tilemap.viewport.y)
        processObjectClick(clickedCell)


def ProcessEvents(elapsed_ms):
    global mouse_click_pos, mouse_is_down
    global current_keys, last_keys
    last_mouse_click_pos[0] = mouse_click_pos[0]
    last_mouse_click_pos[1] = mouse_click_pos[1]
    last_mouse_is_down = mouse_is_down
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_click_pos[0] = event.pos[0]
            mouse_click_pos[1] = event.pos[1]

            mouse_is_down = True
        elif event.type == pygame.MOUSEBUTTONUP:

            mouse_click_pos[0] = -1
            mouse_click_pos[1] = -1

            mouse_is_down = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_is_down:
                mouse_click_pos[0] = event.pos[0]
                mouse_click_pos[1] = event.pos[1]


    last_keys = current_keys
    current_keys = pygame.key.get_pressed()


def RemoveObjectFromMap(object):
    global objectLayer

    if not object == None:
        objectLayer.objects.remove(object)


def setInventoryVisibility(boolean):
    global showInventory
    showInventory = boolean


def printText(msg):
    global font, textLines, textLinesTimeout, textLastText, MAX_TEXT_LINES, DEFAULT_TEXT_TIMEOUT

    while len(textLines) > MAX_TEXT_LINES:
        del textLines[0]
        del textLinesTimeout[0]

    textWhite = font.render(msg, 1,(255, 255, 255))
    text = font.render(msg, 1,(0, 0, 0))
    text.blit(text, (2, 0))
    text.blit(text, (2, 2))
    text.blit(text, (0, 2))
    text.blit(textWhite, (1, 1))
    textLines.append(text)
    textLinesTimeout.append(DEFAULT_TEXT_TIMEOUT)
    textLastText = msg



def Text_Small(text,position,colour):
    text = str(text)
    font_colour = pygame.Color(colour)
    rendered_text = font_Small.render(text, 1, font_colour).convert_alpha()
    screen.blit(rendered_text, position)
    
def Text_Medium(text,position,colour):
    text = str(text)
    font_colour = pygame.Color(colour)
    rendered_text = font_Medium.render(text, 1, font_colour).convert_alpha()
    screen.blit(rendered_text, position)
    
def Text_Large(text,position,colour):
    text = str(text)
    font_colour = pygame.Color(colour)
    rendered_text = font_Large.render(text, 1, font_colour).convert_alpha()
    screen.blit(rendered_text, position)

def DrawScreen():
    global screen
    global tilemap
    global nextPlayerPos
    global player
    global font, textLines, textLinesTimeout, textLastText, lineHeight

    nextPlayerPos.move_ip(-tilemap.viewport.x, -tilemap.viewport.y)

    screen.fill((0,0,0))

    for layer in tilemap.layers:
        if layer.visible:
            layer.draw(screen)
        if layer.name == "objects":
            screen.blit(player, nextPlayerPos)

    if showInventory:
        drawPointer = [screen_size[0] - 48, 48]
        for i in range(1, 10):
             screen.blit(inventoryBox, drawPointer)
             drawPointer[1] = drawPointer[1] + 36

        drawPointer = [screen_size[0] - 48, 48]
        for object in playerInventory:
            screen.blit(object.tile.surface, drawPointer)
            drawPointer[1] = drawPointer[1] + 36

    if len(textLines) > 0:
        for i in range(0, len(textLinesTimeout)):
            textLinesTimeout[i] -= 1

        while len(textLinesTimeout) > 0 and textLinesTimeout[0] <= 0:
            del textLines[0]
            del textLinesTimeout[0]

        if len(textLines) == 0:
            textLastText = ''

    if len(textLines) > 0:
        y = screen.get_size()[1] - len(textLines) * lineHeight
        x = 20

        for text in textLines:
            screen.blit(text, (x, y))
            y = y + lineHeight
