import paho.mqtt.client as mqtt
import pygame, sys, time

pygame.init()

client = mqtt.Client("Controller")

client.connect("172.24.1.184", 1883, 60)

screen = pygame.display.set_mode((64,64))

frameclock = pygame.time.Clock()

straight = True

def moveServo(servo, angle):
    # print(str(servo) + ": " + str(angle))
    client.publish("robot/servo/" + str(servo), str(angle))

def straightenWheels():
    global straight

    moveServo(1, 160)
    moveServo(3, 160)
    moveServo(5, 170)
    moveServo(7, 163)
    if not straight:
        time.sleep(0.5)
        straight = True

def slantWheels():
    global straight

    moveServo(1, 103)
    moveServo(3, 213)
    moveServo(5, 227)
    moveServo(7, 101)
    if straight:
        time.sleep(0.5)
        straight = False

def turnOnSpot(amount):
    if (amount > 0):
        slantWheels()
        moveServo(0, 160)
        moveServo(2, 160)
        moveServo(4, 160)
        moveServo(6, 160)
    elif (amount < 0):
        slantWheels()
        moveServo(0, 145)
        moveServo(2, 145)
        moveServo(4, 145)
        moveServo(6, 145)
    else:
        moveServo(0, 155)
        moveServo(2, 155)
        moveServo(4, 155)
        moveServo(6, 155)

def moveMotors(amount):
    if (amount > 0):
        straightenWheels()
        moveServo(0, 160)
        moveServo(2, 145)
        moveServo(4, 160)
        moveServo(6, 145)
    elif (amount < 0):
        straightenWheels()
        moveServo(0, 145)
        moveServo(2, 160)
        moveServo(4, 145)
        moveServo(6, 160)
    else:
        moveServo(0, 155)
        moveServo(2, 155)
        moveServo(4, 155)
        moveServo(6, 155)


moveMotors(6)
straightenWheels()

servo = 0
angle = 150

while True:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        client.publish("robot/drive", "forward>10")
    elif keys[pygame.K_DOWN]:
        client.publish("robot/drive", "back>10")
    elif keys[pygame.K_LEFT]:
        client.publish("robot/drive", "left>10")
    elif keys[pygame.K_RIGHT]:
        client.publish("robot/drive", "right>10")
    elif keys[pygame.K_a]:
        client.publish("robot/drive", "align")
    elif keys[pygame.K_s]:
        client.publish("robot/drive", "slant")
    else:
        moveMotors(0)

    pygame.display.flip()
    frameclock.tick(30)