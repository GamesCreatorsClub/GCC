import paho.mqtt.client as mqtt

server = input("Connect to -> ")
clientname = input("Connect as -> ")
client = mqtt.Client("Controller")
topicname = input("Select input topic -> ")


client.connect("172.24.1.184", 1883, 60)

while True:
    command = input(clientname + "@" + server + ":" + topicname + "$ ")
    if command == "help":
        print("forward>#")
        print("back>#")
        print("crabLeft>#")
        print("crabRight>#")
        print("pivotLeft>#")
        print("pivotRight>#")
        print("align")
        print("slant")
        print("stop")
        print("sideways")
        print("rotate>3")
    else:
        client.publish(topicname, command)
