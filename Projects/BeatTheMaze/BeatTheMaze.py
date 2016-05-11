import framework
from framework import Left, Right, Up, Down
from framework import playerPos, exitPos, map


def nextPlayerPosition():
    player = playerPos()
    exit = exitPos()

    # Logic to move player around the map goes here



    # And this is result of our computation
    return Left



framework.init(nextPlayerPosition)
framework.mainLoop()
