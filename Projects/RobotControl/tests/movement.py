import time

DELAY = 0.15
FORWARD1 = 160
FORWARD2 = 180
FORWARD3 = 200
BACK1 = 145
BACK2 = 125
BACK3 = 105
STOP = 155
FORWARD = FORWARD3
BACK = BACK3

global moveServo

straight = True

def init(moveServoMethod):
    global moveServo
    moveServo = moveServoMethod
    straightenWheels()

def straightenWheels():
    global moveServo
    global straight, DELAY

    moveServo(1, 160)
    moveServo(3, 160)
    moveServo(5, 170)
    moveServo(7, 163)
    if not straight:
        time.sleep(DELAY)
        straight = True

def slantWheels():
    global moveServo
    global straight, DELAY

    moveServo(1, 103)
    moveServo(3, 213)
    moveServo(5, 227)
    moveServo(7, 101)
    if straight:
        time.sleep(DELAY)
        straight = False

def sidewaysWheels():
    global moveServo
    global straight, DELAY

    moveServo(1, 70)
    moveServo(3, 255)
    moveServo(5, 268)
    moveServo(7, 70)
    if straight:
        time.sleep(DELAY)
        straight = False




def stopAllWheels():
    global moveServo
    moveServo(0, STOP)
    moveServo(2, STOP)
    moveServo(4, STOP)
    moveServo(6, STOP)

def turnOnSpot(amount):
    global moveServo
    forward = STOP + amount
    back = STOP - amount

    slantWheels()
    moveServo(0, back)
    moveServo(2, back)
    moveServo(4, back)
    moveServo(6, back)


def moveMotors(amount):
    global moveServo
    forward = STOP + amount
    back = STOP - amount

    straightenWheels()
    moveServo(0, forward)
    moveServo(2, back)
    moveServo(4, forward)
    moveServo(6, back)

def crabAlong(amount):
    global moveServo
    forward = STOP + amount
    back = STOP - amount

    sidewaysWheels()
    moveServo(0, back)
    moveServo(2, back)
    moveServo(4, forward)
    moveServo(6, forward)
