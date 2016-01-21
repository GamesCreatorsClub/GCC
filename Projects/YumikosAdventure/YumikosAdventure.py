import pygame, sys, math, random

import engine


global screen, screen_size, current_keys, last_keys
global tilemap, playerPos, object, objects, doors, keys

# --------- Important stuff - don't remove ----------------------------------------------------------------

collidedObject = None
collidedTile = None
collidedCell = None

map_names = ["adventure-start.tmx", "first_quest.tmx"]
map_index = 0
current_map = map_names[map_index]

def execute(code):
    exec(code)


def GameInit():
    screen_size = (640, 640)
    engine.Init(screen_size, sys.modules[__name__])


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
    global current_keys, last_keys, tilemap, playerPos, object, objects, mouse_click_pos, mouse_is_down

    elapsed_ms = pygame.time.Clock().tick(60)

    engine.ProcessEvents(elapsed_ms)
    engine.MovePlayer(elapsed_ms)
    engine.DrawScreen()
    
    pygame.display.flip()


# --------- Game methods - add your stuff here ------------------------------------------------------------

def PreventMove():
    engine.moved = False

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
    # TODO implement it properly!!!
    print("Saying '" + msg + "'")
    # engine.drawbubble(10, 10, 200, 200)
    # engine.drawtext(msg)

# --------- Important stuff - don't remove ----------------------------------------------------------------
GameInit()
GameReset()
while True:
    GameLoop()
