import paho.mqtt.client as mqtt
import pygame, os
import agent

pygame.init()

client = mqtt.Client("TestController")

id = "Test"

def onConnect(client, data, rc):
    if rc == 0:
        agent.init(client, id, "TestAgent.py")
    else:
        print("Connection returned error result: " + str(rc))
        os._exit(rc)

def onMessage(client, data, msg):
    global exit

    if agent.process(msg):
        if agent.returncode(id) != None:
            exit = True
    else:
        print("Wrong topic '" + msg.topic + "'")


client.on_connect = onConnect
client.on_message = onMessage

print("Controller: Starting...")

client.connect("gcc-wifi-ap.thenet", 1883, 60)

exit = False

while not exit:
    client.loop()
