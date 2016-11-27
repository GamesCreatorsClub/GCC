 
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SERVO_PIN = 4

client = mqtt.Client("servoSubscriber")

def onConnect(client, data, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("robot/servo/7")


def moveServo(angle):
   f = open("/dev/servoblaster", 'w')
   f.write("7=" + str(angle) + "\n")
   f.close()
   print("moved servo to " + str(angle))
   
def onMessage(client, data, msg):
    print(msg.topic + ": " + str(msg.payload))
    if msg.topic == "robot/servo/7":   
        payload = str(msg.payload,'utf-8')
        moveServo(payload)
        

client.on_connect = onConnect
client.on_message = onMessage

client.connect("localhost", 1883, 60)
client.subscribe("robot/servo/7", 0)

client.loop_forever()
