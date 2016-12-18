import paho.mqtt.client as mqtt
import pygame, sys, os
import agent

pygame.init()

client = mqtt.Client("Controller2")

id = "Drive"


def onConnect(client, data, rc):
    if rc == 0:
        print("Connected")
        agent.init(client, id, "Drive.py")
    else:
        print("Connection returned error result: " + str(rc))
        os._exit(rc)

def onMessage(client, data, msg):
    global exit

    if agent.process(msg):
        if agent.returncode(id):
            exit = True
    else:
        print("Wrong topic '" + msg.topic + "'")


client.on_connect = onConnect
client.on_message = onMessage

print("Controller: Starting...")
client.connect("gcc-wifi-ap.thenet", 1885, 60)

screen = pygame.display.set_mode((600,600))

rects = {
    "UP": pygame.Rect(200, 0, 200, 200),
    "DOWN": pygame.Rect(200, 400, 200, 200),
    "LEFT": pygame.Rect(0, 200, 200, 200),
    "RIGHT": pygame.Rect(400, 200, 200, 200),
    "SPEED": pygame.Rect(200, 200, 200, 200),
}


frameclock = pygame.time.Clock()

straight = True

danceTimer = 0
speed = 10


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                speed = speed - 1
            if event.button == 4:
                speed = speed + 1
            speed = speed % 100
            print("New speed: " + str(speed))

    keys = pygame.key.get_pressed()

    client.loop()
    screen.fill((0, 0, 0))

    if keys[pygame.K_w]:
        client.publish("drive", "forward>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
    elif keys[pygame.K_s]:
        client.publish("drive", "back>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
    elif keys[pygame.K_a]:
        client.publish("drive", "crabLeft>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
    elif keys[pygame.K_d]:
        client.publish("drive", "crabRight>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_q]:
        client.publish("drive", "pivotLeft>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
    elif keys[pygame.K_e]:
        client.publish("drive", "pivotRight>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_x]:
        client.publish("drive", "align")
        pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
        pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
    elif keys[pygame.K_v]:
        client.publish("drive", "slant")
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_SPACE]:
        if danceTimer >= 10:
            client.publish("drive", "slant")
            pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
            pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
            pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
            pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
        elif danceTimer <= 10:
            client.publish("drive", "align")
    elif keys[pygame.K_UP]:
        client.publish("drive", "motors>" + str(speed))
    elif keys[pygame.K_DOWN]:
        client.publish("drive", "motors>" + str(-speed))
    elif keys[pygame.K_i]:
        speed = speed + 10
        if speed > 100:
            speed = 100
        print("New speed: " + str(speed))
    elif keys[pygame.K_o]:
        speed = speed - 10
        if speed < 0:
            speed = 0
        print("New speed: " + str(speed))
    else:
        client.publish("drive", "stop")


    danceTimer += 1
    danceTimer = danceTimer % 20

    value = speed + 155
    if (value > 255):
        value = 255
    elif value < 1:
        value = 0


    pygame.draw.rect(screen, (value, value, value), rects["SPEED"])

    pygame.display.flip()
    frameclock.tick(30)