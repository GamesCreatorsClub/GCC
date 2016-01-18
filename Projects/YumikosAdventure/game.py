import engine

# Important stuff - don't remove

collidedObject = None
collidedTile = None
collidedCell = None

# Game state variables go here





# Important stuff - don't remove

def execute(code):
    exec(code)


# Game state reset
def Reset():
    global collidedCell, collidedTile, collidedObject
    global coins

    coins = 0
    collidedCell = None
    collidedTile = None
    collidedObject = None


# Game methods - add your stuff here

def PreventMove():
    engine.moved = False


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
