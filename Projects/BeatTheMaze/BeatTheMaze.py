import framework
from framework import Left, Right, Up, Down



def nextPlayerPosition():
    player = framework.player_pos()
    exit = framework.exit_pos()

    # Logic to move player around the map goes here



    # And this is result of our computation
    return Left



framework.init(nextPlayerPosition)
framework.mainLoop()
