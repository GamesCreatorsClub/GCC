#!/usr/bin/python3

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import movement
import re


def moveServo(servoid, angle):
    f = open("/dev/servoblaster", 'w')
    f.write(str(servoid) + "=" + str(angle) + "\n")
    f.close()
    print("moved servo " + str(servoid) + " to " + str(angle))


movement.init(moveServo)

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




count = 0

def onConnect(client, data, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("robot/servo/#")


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
            movement.moveMotors(int(args1))
        elif command_name == "back":
            movement.moveMotors(-int(args1))
        elif command_name == "align":
            movement.straightenWheels()
        elif command_name == "slant":
            movement.slantWheels()
        elif command_name == "rotate":
            movement.turnOnSpot(int(args1))
        elif command_name == "pivotLeft":
            movement.turnOnSpot(-int(args1))
        elif command_name == "pivotRight":
            movement.turnOnSpot(int(args1))
        elif command_name == "stop":
            movement.stopAllWheels()
        elif command_name == "sideways":
            movement.sidewaysWheels()
        elif command_name == "crabLeft":
            movement.crabAlong(-int(args1))
        elif command_name == "crabRight":
            movement.crabAlong(int(args1))
        elif command_name == "moveServo":
            moveServo(int(command_args_list[0]), int(command_args_list[0]))



client.on_connect = onConnect
client.on_message = onMessage


client.subscribe("robot/servo/#", 0)
client.subscribe("robot/drive", 0)

def moveServo(servoid, angle):
   f = open("/dev/servoblaster", 'w')
   f.write(str(servoid) + "=" + str(angle) + "\n")
   f.close()
   print("moved servo " + str(servoid) +  " to " + str(angle))



def readSensor():
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
