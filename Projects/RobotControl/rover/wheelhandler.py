storageMap = {}
wheelMap = {}
wheelCalibrationMap = {}

_moveServoMethod = None
DEBUG = False



def initWheel(wheelName, motorServo, steerServo):
    wheelMap[wheelName] = {
        "deg": 0,
        "speed": 0
    }

    defaultWheelCal = {
        "deg": {
            "servo": steerServo,
            "90": "70",
            "0": "160",
            "-90": "230"
        },
        "speed": {
            "servo": motorServo,
            "-300": "95",
            "0": "155",
            "300": "215"
        }
    }

    if wheelName not in wheelCalibrationMap:
        wheelCalibrationMap[wheelName] = defaultWheelCal

    if "deg" not in wheelCalibrationMap[wheelName]:
        wheelCalibrationMap[wheelName]["deg"] = defaultWheelCal["deg"]

    if "speed" not in wheelCalibrationMap[wheelName]:
        wheelCalibrationMap[wheelName]["speed"] = defaultWheelCal["speed"]

    if "servo" not in wheelCalibrationMap[wheelName]["deg"]:
        wheelCalibrationMap[wheelName]["deg"]["servo"] = defaultWheelCal["deg"]["servo"]
    if "90" not in wheelCalibrationMap[wheelName]["deg"]:
        wheelCalibrationMap[wheelName]["deg"]["90"] = defaultWheelCal["deg"]["90"]
    if "0" not in wheelCalibrationMap[wheelName]["deg"]:
        wheelCalibrationMap[wheelName]["deg"]["0"] = defaultWheelCal["deg"]["0"]
    if "-90" not in wheelCalibrationMap[wheelName]["deg"]:
        wheelCalibrationMap[wheelName]["deg"]["-90"] = defaultWheelCal["deg"]["-90"]

    if "servo" not in wheelCalibrationMap[wheelName]["speed"]:
        wheelCalibrationMap[wheelName]["speed"]["servo"] = defaultWheelCal["speed"]["servo"]
    if "-300" not in wheelCalibrationMap[wheelName]["speed"]:
        wheelCalibrationMap[wheelName]["-300"]["servo"] = defaultWheelCal["speed"]["-300"]
    if "0" not in wheelCalibrationMap[wheelName]["speed"]:
        wheelCalibrationMap[wheelName]["speed"]["0"] = defaultWheelCal["speed"]["0"]
    if "300" not in wheelCalibrationMap[wheelName]["speed"]:
        wheelCalibrationMap[wheelName]["speed"]["300"] = defaultWheelCal["speed"]["300"]


def init(moveServoMethod, storageMapIn):
    global _moveServoMethod, storageMap, wheelCalibrationMap

    storageMap = storageMapIn
    _moveServoMethod = moveServoMethod

    if "wheels" not in storageMap:
        storageMap["wheels"] = {}

    if "cal" not in storageMap["wheels"]:
        storageMap["wheels"]["cal"] = {}

    wheelCalibrationMap = storageMap["wheels"]["cal"]

    initWheel("fr", 0, 1)
    initWheel("fl", 2, 3)
    initWheel("br", 4, 5)
    initWheel("bl", 6, 7)

    print("  Started wheelhandler.")


def moveServo(servoNumber, amount):
    if _moveServoMethod == None:
        raise LookupError("Please call wheelhandler.init(moveServoMethod)")

    _moveServoMethod(servoNumber, amount)


def handleWheel(client, topic, payload):
    # wheel/<name>/<deg|speed>

    topicsplit = topic.split("/")
    wheelName = topicsplit[1]
    command = topicsplit[2]

    if wheelName in wheelMap:
        wheel = wheelMap[wheelName]
        wheelCal = wheelCalibrationMap[wheelName]

        if DEBUG:
            print("Handing action: " +  str(topicsplit) + ", " + str(payload))

        if command == "deg":
            if DEBUG:
                print("  Turning wheel: " + wheelName + " to " + str(payload) + " degs")
            handleDeg(wheel, wheelCal["deg"], float(payload))
        elif command == "speed":
            if DEBUG:
                print("  Setting wheel: " + wheelName + " speed to " + str(payload))
            handleSpeed(wheel, wheelCal["speed"], float(payload))
        # if command == "cal":
        #     # wheel/<name>/cal/<command>/position
        #     topiclen = len(topicsplit)
        #     wheelCal = wheel["cal"]
        #
        #     if topiclen < 4: # only cal
        #         m = "deg,90," + str(wheelCal["deg"]["90"]) + "\n"
        #         m = m + "deg,0," + str(wheelCal["deg"]["0"]) + "\n"
        #         m = m + "deg,-90," + str(wheelCal["deg"]["-90"]) + "\n"
        #         m = m + "speed,0," + str(wheelCal["speed"]["0"]) + "\n"
        #         m = m + "speed,300," + str(wheelCal["speed"]["300"]) + "\n"
        #         m = m + "speed,-300," + str(wheelCal["speed"]["-300"]) + "\n"
        #         client.publish("wheel/" + wheelName + "/cal/values", m)
        #
        #     elif topiclen == 5: # calibration for position
        #         command = topicsplit[3]
        #         position = topicsplit[4]
        #
        #
        #         if DEBUG:
        #             print("  Setting wheel " + wheelName + " calibration for " + command + "/" + position + " to " + str(int(payload)))
        #
        #         if command == "deg" or  command == "speed" or command == "servo":
        #             wheelCal[command][position] = int(payload)
        #         else:
        #             wheelCal[command][position] = payload
        #
        #         file = open("rover-calibration.config", 'wb')
        #
        #         pickle.dump(storageMap, file, 0)
        #
        #         file.close()
    else:
        print("ERROR: no wheel with name " +  wheelName + " fonund.")

def handleDeg(wheel, wheelCal, degrees):
    if degrees >= 0:
        servoPosition = interpolate(degrees / 90.0, wheelCal["0"], wheelCal["90"])
    else:
        servoPosition = interpolate((degrees + 90) / 90.0, wheelCal["-90"], wheelCal["0"])

    wheel["deg"] = degrees
    wheel["degsServoPos"] = servoPosition
    servoNumber = wheelCal["servo"]

    moveServo(servoNumber, servoPosition)


def handleSpeed(wheel, wheelCal, speed):

    if speed >= 0:
        servoPosition = interpolate(speed / 300, wheelCal["0"], wheelCal["300"])
    else:
        servoPosition = interpolate((speed + 300) / 300, wheelCal["-300"], wheelCal["0"])

    wheel["speed"] = speed
    wheel["speedServoPos"] = servoPosition
    servoNumber = wheelCal["servo"]

    if str(speed) == "0":
        moveServo(servoNumber, servoPosition)


def interpolate(value, zerostr, maxstr):
    zero = float(zerostr)
    max = float(maxstr)
    return (max - zero) * value + zero

def driveWheel(wheelName):
    wheel = wheelMap[wheelName]
    wheelCal = wheelCalibrationMap[wheelName]["speed"]

    speed = wheel["speed"]
    if "speedServoPos" in wheel:
        servoPosition = wheel["speedServoPos"]

        servoNumber = wheelCal["servo"]

        if str(speed) != "0":
            moveServo(servoNumber, servoPosition)

def driveWheels():
    driveWheel("fl")
    driveWheel("fr")
    driveWheel("bl")
    driveWheel("br")
