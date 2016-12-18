#!/usr/bin/python3

import paho.mqtt.client as mqtt
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

straight = True


def straightenWheels():
    global straight, DELAY

    moveServo(1, 172)
    moveServo(3, 160)
    moveServo(5, 160)
    moveServo(7, 160)
    if not straight:
        time.sleep(DELAY)
        straight = True

def slantWheels():
    global straight, DELAY

    moveServo(1, 103)
    moveServo(3, 213)
    moveServo(5, 227)
    moveServo(7, 101)
    if straight:
        time.sleep(DELAY)
        straight = False


def sidewaysWheels():
    global straight, DELAY

    moveServo(1, 70)
    moveServo(3, 254)
    moveServo(5, 252)
    moveServo(7, 70)
    if straight:
        time.sleep(DELAY)
        straight = False


def stopAllWheels():
    moveServo(0, STOP)
    moveServo(2, STOP)
    moveServo(4, STOP)
    moveServo(6, STOP)


def turnOnSpot(amount):
    forward = STOP + amount
    back = STOP - amount

    slantWheels()
    moveServo(0, back)
    moveServo(2, back)
    moveServo(4, back)
    moveServo(6, back)


def moveMotors(amount):
    forward = STOP + amount
    back = STOP - amount

    moveServo(0, forward)
    moveServo(2, back)
    moveServo(4, forward)
    moveServo(6, back)

def crabAlong(amount):
    forward = STOP + amount
    back = STOP - amount

    sidewaysWheels()
    moveServo(0, back)
    moveServo(2, back)
    moveServo(4, forward)
    moveServo(6, forward)


def moveServo(servoId, angle):
    client.publish("servo/" + str(servoId), str(angle))


client = mqtt.Client("Drive")

def onConnect(client, data, rc):
    client.subscribe("drive/#")
    print("Driver: Connected")
    straightenWheels()


def onMessage(client, data, msg):
    payload = str(msg.payload, 'utf-8')

    if msg.topic == "drive":
        command_name = payload.split(">")[0]
        if len(payload.split(">")) > 1:
            command_args_list = payload.split(">")[1].split(",")
            args1 = command_args_list[0]
        else:
            args1 = 0
        if command_name == "forward":
            straightenWheels()
            moveMotors(int(args1))
        elif command_name == "back":
            straightenWheels()
            moveMotors(-int(args1))
        elif command_name == "motors":
            moveMotors(int(args1))
        elif command_name == "align":
            straightenWheels()
        elif command_name == "slant":
            slantWheels()
        elif command_name == "rotate":
            turnOnSpot(int(args1))
        elif command_name == "pivotLeft":
            turnOnSpot(-int(args1))
        elif command_name == "pivotRight":
            turnOnSpot(int(args1))
        elif command_name == "stop":
            stopAllWheels()
        elif command_name == "sideways":
            sidewaysWheels()
        elif command_name == "crabLeft":
            crabAlong(-int(args1))
        elif command_name == "crabRight":
            crabAlong(int(args1))
        elif command_name == "moveServo":
            moveServo(int(command_args_list[0]), int(command_args_list[0]))



client.on_connect = onConnect
client.on_message = onMessage

print("Driver: Starting...")

client.connect("localhost", 1883, 60)

while True:
    client.loop()

