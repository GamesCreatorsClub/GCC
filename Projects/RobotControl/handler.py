
wheelsMap = {
    "FL": {
        "deg": 0,
        "speed": 0,
        "cal": {
            "deg": {
                "90": 0,
                "0": 0,
                "-90": 0,
                "45": 0
            },
            "speed": {
                "0": 0,
                "10":0,
            }
        },

    },
"BL": {
        "deg": 0,
        "speed": 0,
        "cal": {
            "deg": {
                "90": 0,
                "0": 0,
                "-90": 0,
                "45": 0
            },
            "speed": {
                "0": 0,
                "10":0,
            }
        },

    },
"FR": {
        "deg": 0,
        "speed": 0,
        "cal": {
            "deg": {
                "90": 0,
                "0": 0,
                "-90": 0,
                "45": 0
            },
            "speed": {
                "0": 0,
                "10":0,
            }
        },

    },

"BR": {
        "deg": 0,
        "speed": 0,
        "cal": {
            "deg": {
                "90": 0,
                "0": 0,
                "-90": 0,
                "45": 0
            },
            "speed": {
                "0": 0,
                "10":0,
            }
        },

    }
}

#
# if topic.startswith("wheel/"):
#     handleWheel(topic[6:], payload)

def handleWheel(topic, payload):
    topicsplit = topic.split("/")
    wheelName = topicsplit[0]
    topic = topic.replace(wheelName, "")# cal/speed/100
    if topic.startswith("deg"):
        handleDeg(wheelsMap[wheelName], payload)
    elif topic.startswith("speed"):
        handleSpeed(wheelsMap[wheelName], payload)
    if topic.startswith("cal"):
        handleWheelCalibration(wheelsMap[wheelName], topic, payload);




def handleDeg(wheel, degrees):
    if degrees >= 0:
        servoPosition = findDegFromCallibration(wheel, degrees)

        wheelsMap[wheel]["deg"] = servoPosition
def handleSpeed(wheel, speed):
    wheel["speed"] = int(speed)



def findDeg(toFind, zero, ninety):
    return (ninety - zero) * (toFind / 90) + zero

def findSpeed(toFind, zero, ten):
    return (ten - zero) * (toFind / 90) + zero

def findDegFromCallibration(wheel, toFind):
    return findDeg(toFind, wheelsMap[wheel]["cal"]["deg"]["0"], wheelsMap[wheel]["cal"]["deg"]["90"])

def findSpeedFromCallibration(wheel, toFind):
    return findDeg(toFind, wheelsMap[wheel]["cal"]["speed"]["0"], wheelsMap[wheel]["cal"]["speed"]["10"])



def handleWheelCalibration(wheel, topic, payload):
    deg = int(payload)

    topicsplit = topic.split("/")

    topic = topic.replace("cal", "")
    if topicsplit[1] == "deg":
        deg = int(payload)
        wheelsMap[wheel]["cal"]["deg"][topic] = int(payload)


