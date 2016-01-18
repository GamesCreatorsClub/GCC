import pygame, sys, math, random

import tmx, engine, game


global screen, screen_size, current_keys, last_keys
global tilemap, playerPos, object, objects, doors, keys


def GameInit():
    screen_size = (640, 640)
    engine.Init(screen_size)


def GameReset():
    engine.Reset()
    game.Reset()


def GameLoop():
    global current_keys, last_keys, tilemap, playerPos, object, objects, mouse_click_pos, mouse_is_down

    elapsed_ms = pygame.time.Clock().tick(60)

    engine.ProcessEvents(elapsed_ms)

    engine.MovePlayer(elapsed_ms)
    engine.DrawScreen()
    
    # flip the screen to show our drawing
    pygame.display.flip()


GameInit()
GameReset()
while True:
    GameLoop()
