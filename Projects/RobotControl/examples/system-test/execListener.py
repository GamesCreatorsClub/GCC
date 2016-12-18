import paho.mqtt.client as mqtt
import os, subprocess

client = mqtt.Client("client")

def execute(id, payload):
    text_file = open(str(id)+ ".py", "wt")
    text_file.write(payload)
    text_file.close()

    print("Got msg on topic no " + id)

    subprocessFile = os.popen("python3 " + str(id) + ".py")
    for line in subprocessFile.readlines():
        client.publish("exec/" + str(id) + "/out", line)
        print("exec/" + str(id) + "/out > " + line)

    client.publish("exec/" + str(id) + "/status", "exit")
    print("exec/" + str(id) + "/status > exit")


def onMessage(client, data, msg):
    global dist
    ##print(msg.topic + ": " + str(msg.payload))
    topic = msg.topic
    if topic.startswith("exec/") and topic.endswith("/code"):
        id = topic[5:len(topic) - 5]
        payload = str(msg.payload, 'utf-8')

        execute(id, payload)


client.on_message = onMessage

client.connect("gcc-wifi-ap.thenet", 1883, 60)
client.subscribe("exec/#", 0)

while True:
    # print("loop")
    client.loop()