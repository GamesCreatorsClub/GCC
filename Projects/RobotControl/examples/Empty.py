import paho.mqtt.client as mqtt
import pygame, sys, time


pygame.init()

client = mqtt.Client("MyController3")

client.connect("gcc-robot-3", 1883, 60)

screen = pygame.display.set_mode((600,600))

frameclock = pygame.time.Clock()

def moveServo(servo, angle):
    client.publish("robot/servo/" + str(servo), str(angle))

while True:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

    keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    if keys[pygame.S_w]:
        moveServo(7, 150)

    pygame.display.flip()
    frameclock.tick(30)