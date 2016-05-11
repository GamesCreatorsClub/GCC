import framework
from framework import Left, Right, Up, Down


def nextPlayerPosition():
    return Left


framework.init(nextPlayerPosition)
framework.mainLoop()
