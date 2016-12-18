#!/usr/bin/python3

import subprocess, os
import re
import threading

import paho.mqtt.client as mqtt

client = mqtt.Client("Rover")

SERVO_REGEX = re.compile("servo/(\d)")
DEBUG = True

subprocesses = {}

def execute(id, payload):

    if id in subprocesses:
        oldpopen = subprocesses[id]
        oldpopen.terminate()

    text_file = open(str(id)+ ".py", "wt")
    text_file.write(payload)
    text_file.close()

    print("Got msg on topic no " + id)

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

def onConnect(client, data, rc):
    if rc == 0:
        client.subscribe("exec/#", 0)
        client.subscribe("servo/#", 0)
    else:
        print("Connection returned error result: " + str(rc))
        os._exit(rc)

def onMessage(client, data, msg):
    global dist

    payload = str(msg.payload, 'utf-8')
    topic = msg.topic

    servoMatch = SERVO_REGEX.match(msg.topic)

    if servoMatch:
        servo = int(servoMatch.group(1))
        moveServo(servo, payload)

    elif topic.startswith("exec/") and topic.endswith("/code"):
        id = topic[5:len(topic) - 5]

        thread = threading.Thread(target=execute, args=(id, payload))
        thread.daemon = True
        thread.start()


def moveServo(servoid, angle):
    f = open("/dev/servoblaster", 'w')
    f.write(str(servoid) + "=" + str(angle) + "\n")
    f.close()

client.on_connect = onConnect
client.on_message = onMessage

client.connect("localhost", 1883, 60)


while True:
    client.loop(0.02)
