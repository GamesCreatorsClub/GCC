import paho.mqtt.client as mqtt
import pygame, sys, os

pygame.init()
frameclock = pygame.time.Clock()
bigFont = pygame.font.SysFont("apple casual", 48)
screen = pygame.display.set_mode((600,600))

client = mqtt.Client("CalibrateController")

def onConnect(client, data, rc):
    if rc == 0:
        print("Connected")
    else:
        print("Connection returned error result: " + str(rc))
        os._exit(rc)

wheelsMap = {}

def initWheel(wheelName, motorServo, steerServo):
    global wheelsMap
    wheelsMap[wheelName] = {
        "deg": 0,
        "speed": 0,
        "cal": {
            "deg": {
                "servo": steerServo,
                "90": 70,
                "0": 160,
                "-90": 230
            },
            "speed": {
                "servo": motorServo,
                "-300": 95,
                "0": 155,
                "300":215
            }
        }
    }

initWheel("fr", 0, 1)
initWheel("fl", 2, 3)
initWheel("br", 4, 5)
initWheel("bl", 6, 7)

client.on_connect = onConnect

print("CalibrateController: Starting...")
client.connect("172.24.1.185", 1883, 60)


degs = ["-90", "-45", "0", "45", "90"]
degsCal = ["-90", "-90", "0", "90", "90"]
degInitValues = []
speeds = ["-300", "-200", "-150", "-100", "-75", "-50", "0", "50", "75", "100", "150", "200", "300"]
speedsCal = ["-300", "-300", "-300", "-300", "-300", "-300", "0", "300", "300", "300", "300", "300", "300"]


wheel = "bl"
degIndex = 2
speedIndex = 5


keys = []
lastKeys = []

speedChange = False
degChange = True

degValue = 0
speedValue = 0

sendChanges = False


def storeValue():
    wheelsMap[wheel]["cal"]["deg"][degsCal[degIndex]] = degValue
    wheelsMap[wheel]["cal"]["speed"][speedsCal[speedIndex]] = speedValue


def fetchValue():
    global degValue, speedValue

    degValue = wheelsMap[wheel]["cal"]["deg"][degsCal[degIndex]]
    speedValue = wheelsMap[wheel]["cal"]["speed"][speedsCal[speedIndex]]

fetchValue()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    client.loop(timeout=1/20.0)
    screen.fill((0, 0, 0))

    if keys != lastKeys:
        lastKeys = keys[:]

        if keys[pygame.K_1]:
            wheel = "fr"
            fetchValue()
        elif keys[pygame.K_2]:
            wheel = "fl"
            fetchValue()
        elif keys[pygame.K_3]:
            wheel = "br"
            fetchValue()
        elif keys[pygame.K_4]:
            wheel = "bl"
            fetchValue()

        elif keys[pygame.K_q]:
            if degIndex > 0:
                degIndex = degIndex - 1
                degChange = True
                fetchValue()
        elif keys[pygame.K_e]:
            if degIndex < 4:
                storeValue()
                degIndex = degIndex + 1
                degChange = True
                fetchValue()

        elif keys[pygame.K_w]:
            if speedIndex > 0:
                speedIndex = speedIndex - 1
                speedChange = True
                fetchValue()
        elif keys[pygame.K_s]:
            if speedIndex < 12:
                storeValue()
                speedIndex = speedIndex + 1
                speedChange = True
                fetchValue()


        elif keys[pygame.K_o]:
            if degValue > 50:
                storeValue()
                degValue = degValue - 1
                degChange = True
        elif keys[pygame.K_p]:
            if degValue < 300:
                storeValue()
                degValue = degValue + 1
                degChange = True


        elif keys[pygame.K_k]:
            if speedValue > 50:
                storeValue()
                speedValue = speedValue - 1
                speedChange = True
        elif keys[pygame.K_l]:
            if speedValue < 300:
                storeValue()
                speedValue = speedValue + 1
                speedChange = True


        elif keys[pygame.K_r]:
            t1 = wheelsMap[wheel]["cal"]["deg"]["90"]
            t2 = wheelsMap[wheel]["cal"]["deg"]["-90"]
            wheelsMap[wheel]["cal"]["deg"]["90"] = t2
            wheelsMap[wheel]["cal"]["deg"]["-90"] = t1

        elif keys[pygame.K_f]:
            t1 = wheelsMap[wheel]["cal"]["speed"]["300"]
            t2 = wheelsMap[wheel]["cal"]["speed"]["-300"]
            wheelsMap[wheel]["cal"]["speed"]["300"] = t2
            wheelsMap[wheel]["cal"]["speed"]["-300"] = t1

        elif keys[pygame.K_z]:
            sendChanges = False
        elif keys[pygame.K_x]:
            sendChanges = True


    text = bigFont.render("Wheel: " + wheel, 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 0, 0, 0))

    text = bigFont.render("Angle: " + degs[degIndex], 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 40, 0, 0))

    text = bigFont.render("Angle calibrating: " + degsCal[degIndex], 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 70, 0, 0))

    text = bigFont.render("Angle servo: " + str(degValue), 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 100, 0, 0))

    text = bigFont.render("Speed: " + speeds[speedIndex], 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 140, 0, 0))

    text = bigFont.render("Speed calibrating: " + speedsCal[speedIndex], 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 170, 0, 0))

    text = bigFont.render("Speed servo: " + str(speedValue), 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 200, 0, 0))

    text = bigFont.render("Send changes: " + str(sendChanges), 1, (255, 255, 255))
    screen.blit(text, pygame.Rect(0, 240, 0, 0))


    if degChange:
        client.publish("wheel/" + wheel + "/deg", degs[degIndex])
        if sendChanges:
            client.publish("wheel/" + wheel + "/cal/deg/" + degsCal[degIndex], degValue)

    #if speedChange:
    #    client.publish("wheel/" + wheel + "/speed", degs[speedIndex])
    #    client.publish("wheel/" + wheel + "/cal/speed/" + speedsCal[speedIndex], speedValue)


    pygame.display.flip()
    frameclock.tick(30)