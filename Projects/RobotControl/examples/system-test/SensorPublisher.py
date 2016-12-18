
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print("Distance measurement in progress")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(0.5)

client = mqtt.Client("sensor_pub")

client.connect("localhost", 1883, 60)

count = 0

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
    distance = read()
    if distance < 10:
      distance = 10.0
    if distance > 800:
      distance = 800.0
    time.sleep(.020)
    client.publish("robot/sensors/distance", "distance=" + str(distance))

