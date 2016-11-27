#!/usr/bin/python

import pygame
import RPi.GPIO as GPIO
import time, math

pygame.init()
screen = pygame.display.set_mode((500,500))
frame_clock = pygame.time.Clock()


GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

SERVO_PIN = 4

print("Distance measurement in progress")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(1)

readings = {}

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
servoAngle = 90
while True:
   for event in pygame.event.get():
      if event == pygame.QUIT:
         pygame.exit()

   distance = read()

   if distance > 10 and distance < 800:
      print("Distance:" + toStr(distance) + "mm at angle " + str(servoAngle))
      readings[servoAngle] = (255, distance)

   moveServo(servoAngle)
   servoAngle = servoAngle + direction
   if servoAngle == 180:
       direction = -1
   if servoAngle == 90:
       direction = 1
      
   screen.fill((0,0,0))

   for a in readings:
      v = readings[a]
      c = v[0]
      c = c - 5
      if c < 50:
         c = 50
      readings[a] = (c, v[1])
      
      d = v[1] / 2
 
      ar = a * math.pi / 180 + math.pi /4

      x = 250 + d * math.sin(ar)
      y = 250 + d * math.cos(ar)
      
      # pygame.draw.line(screen, (0,255,0),(x, y),(x, y) )
      pygame.draw.circle(screen, (0, v[0], 0), (int(x), int(y)), 2)
      pygame.draw.circle(screen, (0, 255, 0), (250, 250), 2)
   
   pygame.display.flip()
   frame_clock.tick()
   time.sleep(0.1)

GPIO.cleanup()
