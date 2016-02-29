import pygame, sys, math, random

import engine


global screen, screen_size, current_keys, last_keys
global tilemap, object, objects, doors, keys

# --------- Important stuff - don't remove ----------------------------------------------------------------

pygame.init()

animatedObject = None
collidedObject = None
collidedTile = None
collidedCell = None
clickedObject = None

map_names = ["start.tmx", "example-map.tmx", "first-quest.tmx"]
map_index = 0
current_map = map_names[map_index]

pygame.mixer.pre_init()
pygame.mixer.init()

noPlayerInput = False

# change file for different music
music = pygame.mixer.music.load("music.wav")
screen_size = (640, 640)

frameclock = pygame.time.Clock()

def execute(code):
    exec(code)


def GameInit():
    global screen_size
    engine.Init(screen_size, sys.modules[__name__])
    ##pygame.mixer.music.play(-1)


def GameReset():
    global collidedCell, collidedTile, collidedObject
    global currentMap
    global coins

    engine.Reset()
    engine.LoadMap(map_names[map_index])

    coins = 0
    collidedCell = None
    collidedTile = None
    collidedObject = None


def GameLoop():
    global current_keys, last_keys, tilemap, object, objects, mouse_click_pos, mouse_is_down, noPlayerInput, fps

    elapsed_ms = frameclock.tick(60)
    fps = frameclock.get_fps()

    engine.Animate()
    engine.ProcessEvents(elapsed_ms)
    if not noPlayerInput:
        engine.MovePlayerWithKeys(elapsed_ms)

    engine.ProcessClick(elapsed_ms)
    engine.DrawScreen()

    pygame.display.flip()


# --------- Game methods - add your stuff here ------------------------------------------------------------

def PreventMove():
    engine.moved = False


def teleportToObject(name):
    engine.teleportToObject(name)


def NextMap():
    global map_index, map_names

    map_index = map_index + 1
    if map_index == len(map_names):
        map_index = 0

    Map(map_names[map_index])


def Map(name):
    engine.LoadMap(name)


def AddCoins(amount):
    global coins

    coins = coins + 1


def RemoveCoins(amount):
    global coins

    coins = coins - 1
    if coins < 0:
        coins = 0


def Pay(amount):
    if coins >= amount:
        RemoveCoins(amount)
        return True
    return False


def RemoveCollidedObject():
    global collidedObject

    objectsLayer = engine.tilemap.layers["objects"]
    objectsLayer.objects.remove(collidedObject)


def Say(msg):
    engine.printText(msg)

def SayOnce(msg):
    if engine.textLastText != msg:
        engine.printText(msg)

def GetInventory():
    return engine.playerInventory


def InventoryContains(objectName):
    for object in engine.playerInventory:
        if object.name == objectName:
            return True

    return False

def AddObjectToInventory(object):
    engine.playerInventory.append(object)
    engine.RemoveObjectFromMap(object)


def RemoveObjectFromInventory(object):
    engine.playerInventory.remove(object)


def GiveObject(objectName):
    object = engine.objectLayer.find_by_name(objectName)
    if object != None:
        AddObjectToInventory(object)


def SetInventoryVisibility(boolean):
    engine.setInventoryVisibility(boolean)


def PushableObject():
    MoveObjectAway(collidedObject)
    PreventMove()

def MoveObjectAway(gameObject):
    if engine.playerCollideRect.right < gameObject.px:
        gameObject.px += 4
    elif engine.playerCollideRect.left > gameObject.px + gameObject.width:
        gameObject.px -= 4

    if engine.playerCollideRect.bottom < gameObject.py:
        gameObject.py += 4
    elif engine.playerCollideRect.top > gameObject.py + gameObject.height:
        gameObject.py -= 4


def DistanceFromPlayer(gameObject):
    py1 = engine.playerCollideRect.top
    px = (engine.playerCollideRect.left + engine.playerCollideRect.right) / 2
    py = (engine.playerCollideRect.top + engine.playerCollideRect.bottom) / 2

    ox = gameObject.px + gameObject.width / 2
    oy = gameObject.py + gameObject.height / 2

    return Distance(px, py, ox, oy)

def DistanceBetweenObjects(gameObject1, gameObject2):
    return Distance(gameObject1.px, gameObject1.py, gameObject2.px, gameObject2.py);

def Distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


# --------- Important stuff - don't remove ----------------------------------------------------------------
GameInit()
GameReset()
while True:
    GameLoop()
