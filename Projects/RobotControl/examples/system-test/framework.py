import paho.mqtt.client as mqtt

global client, exit

client = mqtt.Client("sender")
exit = False

def onConnect(client, data, rc):
    if rc == 0:
        client.subscribe("exec/#", 0)
    else:
        print("Connection returned error result: " + str(rc))
        os._exit(rc)

def onMessage(client, data, msg):
    global exit

    if msg.topic.endswith("/out"):
        payload = str(msg.payload, 'utf-8')
        print(payload)
    elif msg.topic.endswith("/status"):
        payload = str(msg.payload, 'utf-8')
        if payload == "exit":
            exit = True
    else:
        print("Wrong topic '" + msg.topic + "'")

def sendFile(name, id, robot="gcc-wifi-ap.thenet"):
    client.connect(robot, 1883, 60)
    client.subscribe("exec/" + str(id) + "/#", 0)

    file = open(name)
    fileContent = file.read()
    file.close()

    client.publish("exec/" + str(id) + "/code", fileContent)

    print("Sent file " + name + " to " + robot + " on topic exec/" + str(id) + "/code")

client.on_connect = onConnect
client.on_message = onMessage

sendFile("test.py", 5)

while not exit:
    client.loop()