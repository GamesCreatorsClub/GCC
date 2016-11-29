#!/usr/bin/python3

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

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

count = 0
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
        client.publish("robot/sensors/distance", str(distance))
        print("Published: " + "robot/sensors/distance as distance=" + str(distance))
        

client.on_connect = onConnect
client.on_message = onMessage


client.subscribe("robot/servo/7", 0)




def read():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    while GPIO.input(ECHO) == 0 and time.time() - start < 0.1:
        pass

    pulse_start = time.time()

    while GPIO.input(ECHO) == 1 and time.time() - start < 2:
        pass

    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 171500

    distance = round(distance, 2)

    return distance

while True:
    client.loop()
    distance = read()
    if distance < 10:
      distance = 10.0
    if distance > 800:
      distance = 800.0

    client.publish("robot/sensors/distance", str(distance))
    print("Published: " + "robot/sensors/distance as distance=" + str(distance))

    time.sleep(.02)

GPIO.cleanup() 
