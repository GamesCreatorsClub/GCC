import paho.mqtt.client as mqtt
import pygame, sys, time

pygame.init()

client = mqtt.Client("Controller")

client.connect("172.24.1.184", 1883, 60)

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

angle = 155
def moveServo(servo, angle):
    print(str(servo) + ": " + str(angle))
    client.publish("robot/servo/" + str(servo), str(angle))



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
    keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    if keys[pygame.K_w]:
        client.publish("robot/drive", "forward>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
    elif keys[pygame.K_s]:
        client.publish("robot/drive", "back>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
    elif keys[pygame.K_a]:
        client.publish("robot/drive", "crabLeft>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
    elif keys[pygame.K_d]:
        client.publish("robot/drive", "crabRight>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_q]:
        client.publish("robot/drive", "pivotLeft>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
    elif keys[pygame.K_e]:
        client.publish("robot/drive", "pivotRight>" + str(speed))
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_x]:
        client.publish("robot/drive", "align")
        pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
        pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
    elif keys[pygame.K_v]:
        client.publish("robot/drive", "slant")
        pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
        pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
    elif keys[pygame.K_SPACE]:
        if danceTimer >= 10:
            client.publish("robot/drive", "slant")
            pygame.draw.rect(screen, (255, 255, 255), rects["UP"])
            pygame.draw.rect(screen, (255, 255, 255), rects["DOWN"])
            pygame.draw.rect(screen, (255, 255, 255), rects["LEFT"])
            pygame.draw.rect(screen, (255, 255, 255), rects["RIGHT"])
        elif danceTimer <= 10:
            client.publish("robot/drive", "align")
    else:
        client.publish("robot/drive", "stop")
    #
    # servo = 7
    # if keys[pygame.K_UP]:
    #
    #     angle = angle + 1
    #     moveServo(servo, angle)
    # if keys[pygame.K_DOWN]:
    #     angle = angle - 1
    #     moveServo(servo, angle)
    #


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