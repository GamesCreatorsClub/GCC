import pygame, sys, math, random

import paho.mqtt.client as mqtt

client = mqtt.Client("client")

def onConnect(client, data, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("robot/sensors/distance")

def onMessage(client, data, msg):
    global dist
    print(msg.topic + ": " + str(msg.payload))
    if msg.topic == "robot/sensors/distance":
        payload = str(msg.payload, 'utf-8')
        dist = float(payload)
        dist = dist / 4.0

client.on_connect = onConnect
client.on_message = onMessage

client.connect("gcc-robot-2.thenet", 1883, 60)
client.subscribe("robot/sensors/distance", 0)





pygame.init()

global screen, size, centre, points, dist

size = [640, 480]
centre = (size[0]/ 2, size[1] / 2)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')

frameclock = pygame.time.Clock()

points = []


def getRadarAngle(angle, distance=180):
    angle = angle * math.pi / 180
    ey = math.sin(angle) * distance
    ex = math.cos(angle) * distance

    end = (size[0]/ 2 + ex, size[1] / 2 + ey)
    return end

def addRadarPoint(angle, distance):
    for point in points:
        if (point["angle"] == angle):
            point["life"] = 0
    pos = getRadarAngle(angle, distance)
    point = {
        "pos": (int(pos[0]), int(pos[1])),
        "dist": distance,
        "angle": angle,
        "life": 255
    }

    points.append(point)

def drawpoints(points):

   # list = []
    for point in points:#range(len(points) -1, -1, -1):
        #point = points[i]
        #list.append(point["pos"])
        point["life"] -= 1
        if (point["life"] < 0):
             del point
        else:
             div = 200
             life = ( point["life"]) / 255
             color = ( (((div - point["dist"]) / div) * 255) * life , (((point["dist"]) / div) * 255) * life, 0)
             pygame.draw.circle(screen, color, point["pos"], 4)
    # if (len(list) > 2):
    #    pygame.draw.lines(screen, (255,255,255), False, list, 1)
    main_point = points[len(points) -1]
    pygame.draw.line(screen, (255,255,255), centre, main_point["pos"], 4)





deg = 90
direction = 1
dist = 30

while True:
    client.loop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    client.publish("robot/servo/7", str(deg))
    deg = deg + direction
    if deg >= 180:
         direction = -1
    if deg <= 90:
         direction = 1


    screen.fill((0, 0, 0))
    # deg = deg + direction
    # deg = deg % 90
    # dist += 1
    addRadarPoint(-deg + 45, dist)
    drawpoints(points)


    pygame.display.update()
    frameclock.tick(20)



