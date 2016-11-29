#!/usr/bin/python3

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import re


GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

SERVO_PIN = 4

print("Distance measurement in progress")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(0.5)


client = mqtt.Client("Robot")

client.connect("localhost", 1883, 60)


sbscribedservos = [0, 1, 2, 3, 4, 5, 6, 7]

servoRegex = re.compile("robot/servo/(\d)")

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
count = 0

def onConnect(client, data, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("robot/servo/#")


def moveServo(servoid, angle):
   f = open("/dev/servoblaster", 'w')
   f.write(str(servoid) + "=" + str(angle) + "\n")
   f.close()
   print("moved servo " + str(servoid) +  " to " + str(angle))
   
def onMessage(client, data, msg):
    payload = str(msg.payload, 'utf-8')

    print(msg.topic + ": " + payload)
    m = servoRegex.match(msg.topic)

    if m:
        servo = int(m.group(1))
        moveServo(servo, payload)
        # client.publish("robot/sensors/distance", str(distance))
        # print("Published: " + "robot/sensors/distance as distance=" + str(distance))
    elif msg.topic == "robot/drive":
        command_name = payload.split(">")[0]
        if len(payload.split(">")) > 1:
            command_args_list = payload.split(">")[1].split(",")
            args1 = command_args_list[0]
        else:
            args1 = 0
        if command_name == "forward":
            moveMotors(int(args1))
        elif command_name == "back":
            moveMotors(-int(args1))
        elif command_name == "align":
            straightenWheels()
        elif command_name == "slant":
            slantWheels()
        elif command_name == "rotate":
            turnOnSpot(int(args1))
        elif command_name == "left":
            turnOnSpot(-int(args1))
        elif command_name == "right":
            turnOnSpot(int(args1))
        elif command_name == "stop":
            stopAllWheels()



client.on_connect = onConnect
client.on_message = onMessage


client.subscribe("robot/servo/#", 0)
client.subscribe("robot/drive", 0)

def straightenWheels():
    global straight, DELAY

    moveServo(1, 160)
    moveServo(3, 160)
    moveServo(5, 170)
    moveServo(7, 163)
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

def stopAllWheels():
    moveServo(0, STOP)
    moveServo(2, STOP)
    moveServo(4, STOP)
    moveServo(6, STOP)

def turnOnSpot(amount):
    forward = FORWARD1
    back = BACK1
    if (amount < 0):
        slantWheels()
        moveServo(0, forward)
        moveServo(2, forward)
        moveServo(4, forward)
        moveServo(6, forward)
    elif (amount > 0):
        slantWheels()
        moveServo(0, back)
        moveServo(2, back)
        moveServo(4, back)
        moveServo(6, back)
    else:
        moveServo(0, STOP)
        moveServo(2, STOP)
        moveServo(4, STOP)
        moveServo(6, STOP)

def moveMotors(amount):
    forward = FORWARD
    back = BACK
    if (amount > 0):
        straightenWheels()
        moveServo(0, forward)
        moveServo(2, back)
        moveServo(4, forward)
        moveServo(6, back)
    elif (amount < 0):
        straightenWheels()
        moveServo(0, back)
        moveServo(2, forward)
        moveServo(4, back)
        moveServo(6, forward)
    else:
        moveServo(0, STOP)
        moveServo(2, STOP)
        moveServo(4, STOP)
        moveServo(6, STOP)



def read():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    while GPIO.input(ECHO) == 0 and time.time() - start < 0.1:
        pass

    pulse_start = time.time()

    while GPIO.input(ECHO) == 1 and time.time() - start < 0.3:
        pass

    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 171500

    distance = round(distance, 2)

    return distance

while True:
    client.loop()
    # distance = read()
    # if distance < 10:
    #   distance = 10.0
    # if distance > 800:
    #   distance = 800.0
    # time.sleep(.02)
    

GPIO.cleanup() 
