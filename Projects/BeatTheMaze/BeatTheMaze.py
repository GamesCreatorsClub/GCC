import framework
from framework import Left, Right, Up, Down
from framework import playerPos, exitPos, map


def nextPlayerPosition():
    player = playerPos()
    exit = exitPos()

    # Use player.x and player.y to find player position
    # Use exit.x and exit.y to find exit position
    # Use map(Left), map(Right), map(Up) or map(Down) to
    #     find out if given move is valid. Method map() will return True or False
    # Use mapAt(x, y) to check if particular cell of the map has obstacle or not.
    #     If there is NO obstacle it will return True and False otherwise

    # Keys when game is running:
    #     ESC - leaves the game
    #     SPACE - advances player one step
    #     RETURN/ENTER - moves player all way to the exit
    #
    # If player leaves map/screen it is game over
    # If player moves twice more time than there are squares on the map it is game over

    # Logic to move player around the map goes here:




    # And this is result of our computation
    return Left



framework.init(nextPlayerPosition)
framework.mainLoop()
