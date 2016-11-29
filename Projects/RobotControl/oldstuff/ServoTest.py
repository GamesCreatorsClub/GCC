#!/usr/bin/python3

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

def moveServo(angle):
   f = open("/dev/servoblaster", 'w')
   f.write("7=" + str(angle) + "\n")
   f.close()
   #print("Servo to " + str(angle))

def toStr(n):
    s = str(n)
    i = s.index('.')
    l = len(s)
    if i + 2 >= l:
        s = s + '0'
        l = l + 1
    if i + 2 >= l:
        s = s + '0'
        l = l + 1
    while l < 8:
        s = ' ' + s
        l = l + 1
    return s

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

direction = 1
servoAngle = 80
while True:
    distance = read()
    if distance < 10:
      distance = 10.0
    if distance > 800:
      distance = 800.0

    print("Distance:" + toStr(distance) + "mm at angle " + str(servoAngle))

    moveServo(servoAngle)
    servoAngle = servoAngle + direction
    if servoAngle == 200:
        direction = -1
    if servoAngle == 80:
        direction = 1

    time.sleep(0.1)

GPIO.cleanup()
