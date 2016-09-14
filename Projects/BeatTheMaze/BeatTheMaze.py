import framework, pygame
from framework import Left, Right, Up, Down
from framework import playerPos, exitPos, map, mapAt, keys
from framework import lastBreadcrumb, goBack, currentBreadcrumb, hasVisited, addBreadcrumb

def nextPlayerPosition():

    player = playerPos()
    exit = exitPos()

    # Use player.x and player.y to find player position
    # Use exit.x and exit.y to find exit position
    # Use map(Left), map(Right), map(Up) or map(Down) to
    #     find out if given move is valid. Method map() will return True or False
    # Use mapAt(x, y) to check if particular cell of the map has obstacle or not.
    #     If there is NO obstacle it will return True and False otherwise

    # Breadcrumb methods:
    #
    # hasVisited(direction) returns True or False depending if direction relative to the
    #     player has been visited or not
    # hasVisited(x, y) same as above but for arbitrary cell
    # goBack() returns direction to previously visited cell and removes breadcrumb (current position)
    # currentBreadcrumb() returns what is breadcrumb at place player is standing on
    # addBreadcrumb() adds breadcrumb at position players is on

    # breadcrumb[0] = x coordinate
    # breadcrumb[1] = y coordinate
    # breadcrumb[2] = last direction player has gone to from that cell
    # breadcrumb[0] = first (original) direction player has gone to from that cell


    # Keys when game is running:
    #     ESC - leaves the game
    #     SPACE - advances player one step
    #     RETURN/ENTER - moves player all way to the exit
    #
    # If player leaves map/screen it is game over
    # If player moves twice more time than there are squares on the map it is game over

    # Logic to move player around the map goes here:
    if player.x < exit.x:
        return Right

    return Left


def turn(direction):
    if direction == Down:
        return Left
    if direction == Left:
        return Up
    if direction == Up:
        return Right

    return Down


framework.init(nextPlayerPosition)
framework.mainLoop()
