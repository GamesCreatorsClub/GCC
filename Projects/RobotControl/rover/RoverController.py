#!/usr/bin/python3

import subprocess, os
import re
import threading

import paho.mqtt.client as mqtt
import pickle
import os.path
import RPi.GPIO as GPIO
import time

import wheelhandler


SERVO_REGEX = re.compile("servo/(\d+)")
DEBUG = True
SWITCH_GPIO = 20
CAMERA_LIGHT_GPIO = 16
wheelhandler.DEBUG = DEBUG

lightsState = False

storageMap = {}
subprocesses = {}

GPIO.setmode(GPIO.BCM)
GPIO.setup(CAMERA_LIGHT_GPIO, GPIO.OUT)
GPIO.setup(SWITCH_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def init():
    if os.path.exists("rover-storage.config"):
        file = open("rover-storage.config", "rb")
        loaded = pickle.load(file)
        file.close()

        if DEBUG:
            print("  Loaded " +  str(loaded))

        for key in loaded:
            storageMap[key] = loaded[key]

        print("  Storage map is " + str(storageMap))


print("Starting RoverController...")

init()

client = mqtt.Client("Rover")



def execute(id, payload):

    if id in subprocesses:
        oldpopen = subprocesses[id]
        oldpopen.terminate()

    text_file = open(str(id)+ ".py", "wt")
    text_file.write(payload)
    text_file.close()

    if DEBUG:
        print("Got msg on topic no " + id)

    print("Starting new agent " + id )

    popen = subprocess.Popen(["python3",  str(id) + ".py"], stdout = subprocess.PIPE, universal_newlines = True)

    subprocesses[id] = popen

    textStream = popen.stdout

    popen.poll()
    while popen.returncode == None:
        line = textStream.readline()
        client.publish("exec/" + str(id) + "/out", str(line))
        if DEBUG:
            if line.endswith("\n"):
                print("exec/" + str(id) + "/out > " + str(line), end="")
            else:
                print("exec/" + str(id) + "/out > " + str(line))
        popen.poll()

    for line in textStream.readlines():
        if len(len) > 0:
            client.publish("exec/" + str(id) + "/out", str(line))
            if DEBUG:
                if line.endswith("\n"):
                    print("exec/" + str(id) + "/out > " + str(line), end="")
                else:
                    print("exec/" + str(id) + "/out > " + str(line))

    del subprocesses[id]

    client.publish("exec/" + str(id) + "/status", str(popen.returncode))
    if DEBUG:
        print("exec/" + str(id) + "/status > " + str(popen.returncode))

def setLights(state):
    global lightsState

    lightsState = state
    GPIO.output(CAMERA_LIGHT_GPIO, state)


def prepareToShutdown():
    previousLightsState = lightsState
    seconds = 0.0
    interval = 0.3
    state = True
    while seconds <= 6.0 and GPIO.input(SWITCH_GPIO) == 0:
        time.sleep(interval)
        seconds = seconds + interval
        setLights(state)
        state = not state

    if GPIO.input(SWITCH_GPIO) == 0:
        doShutdown()
    else:
        setLights(previousLightsState)

def doShutdown():
    print("Shutting down now!")
    subprocess.call(["/usr/bin/sudo", "/sbin/shutdown", "-h", "now"])

def handleSystemMessages(topic, payload):
    print("Got system message on " + topic + ": " + payload)
    if topic == "shutdown" and payload == "secret_message":
        doShutdown()

def composeRecursively(map, prefix):
    res = ""
    for key in map:
        if type(map[key]) is dict:
            newPrefix = prefix + key + "/"
            res = res + composeRecursively(map[key], newPrefix)
        else:
            res = res + prefix + key + "=" + str(map[key]) + "\n"

    return  res

def readoutStorage():
    client.publish("storage/values", composeRecursively(storageMap, ""))

def writeStorage(topicsplit, value):
    map = storageMap
    for i in range(2, len(topicsplit) - 1):
        key = topicsplit[i]
        if key not in map:
            map[key] = {}
        map = map[key]
    key = topicsplit[len(topicsplit) - 1]
    map[key] = value

    if DEBUG:
        print("Storing to storage " + str(topicsplit) + " = " + value)

    file = open("rover-storage.config", 'wb')

    pickle.dump(storageMap, file, 0)

    file.close()

def onConnect(client, data, rc):
    if rc == 0:
        client.subscribe("system/+", 0)
        client.subscribe("exec/+/code", 0)
        client.subscribe("servo/+", 0)
        client.subscribe("wheel/+/deg", 0)
        client.subscribe("wheel/+/speed", 0)
        client.subscribe("storage/write/#", 0)
        client.subscribe("storage/read", 0)
        client.subscribe("lights/#", 0)
    else:
        print("ERROR: Connection returned error result: " + str(rc))
        os._exit(rc)

def onMessage(client, data, msg):
    global dist

    payload = str(msg.payload, 'utf-8')
    topic = msg.topic


    if  topic.startswith("wheel/"):
        wheelhandler.handleWheel(client, topic, payload)
    else:
        servoMatch = SERVO_REGEX.match(msg.topic)
        if servoMatch:
            servo = int(servoMatch.group(1))
            # print("servo matched: " + topic + ", servo " + str(servo))
            moveServo(servo, payload)

        elif topic.startswith("exec/") and topic.endswith("/code"):
            id = topic[5:len(topic) - 5]

            thread = threading.Thread(target=execute, args=(id, payload))
            thread.daemon = True
            thread.start()
        elif topic.startswith("system/"):
            handleSystemMessages(topic[7:], payload)
        elif topic.startswith("storage/"):
            topicsplit = topic.split("/")
            if topicsplit[1] == "read":
                if DEBUG:
                    print("Reading out storage")
                readoutStorage()
            elif topicsplit[1] == "write":
                writeStorage(topicsplit, payload)
        elif topic.startswith("lights/"):
            topicsplit = topic.split("/")
            if topicsplit[1] == "camera":
                if "on" == payload or "ON" == payload or "1" == payload:
                    setLights(True)
                else:
                    setLights(False)

def moveServo(servoid, angle):
    f = open("/dev/servoblaster", 'w')
    f.write(str(servoid) + "=" + str(angle) + "\n")
    f.close()

client.on_connect = onConnect
client.on_message = onMessage

client.connect("localhost", 1883, 60)

wheelhandler.init(moveServo, storageMap)

print("Started RoverController.")

setLights(lightsState)

while True:
    client.loop(0.02)
    wheelhandler.driveWheels()
    if GPIO.input(SWITCH_GPIO) == 0:
        prepareToShutdown()