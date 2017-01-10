import pickle
import os.path

storageMap = {}
_moveServoMethod = None
DEBUG = False

def initWheel(wheelName, motorServo, steerServo):
    global storageMap
    storageMap[wheelName] = {
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


def init(moveServoMethod):
    global _moveServoMethod
    global storageMap

    _moveServoMethod = moveServoMethod

    initWheel("fr", 0, 1)
    initWheel("fl", 2, 3)
    initWheel("br", 4, 5)
    initWheel("bl", 6, 7)

    if os.path.exists("rover-calibration.config"):
        file = open("rover-calibration.config", "rb")
        loaded = pickle.load(file)
        file.close()

        if DEBUG:
            print("Managed to load " +  str(loaded))

        for wheelName in loaded:
            for wk in loaded[wheelName]:
                if wk == "cal":
                    storageMap[wheelName]["cal"] = loaded[wheelName][wk]

        print("Started wheelhandler. Wheels map is " + str(storageMap))

def moveServo(servoNumber, amount):
    global _moveServoMethod
    if _moveServoMethod == None:
        raise LookupError("Please call wheelhandler.init(moveServoMethod)")

    _moveServoMethod(servoNumber, amount)


def handleWheel(client, topic, payload):
    global storageMap

    # storage/write/<object>/<command>

    topicsplit = topic.split("/")
    wheelName = topicsplit[1]
    command = topicsplit[2]

    if wheelName in storageMap:
        wheel = storageMap[wheelName]

        if DEBUG:
            print("Handing action: " +  str(topicsplit) + ", " + str(payload))

        if command == "deg":
            if DEBUG:
                print("  Turning wheel: " + wheelName + " to " + str(payload) + " degs")
            handleDeg(wheel, float(payload))
        elif command == "speed":
            if DEBUG:
                print("  Setting wheel: " + wheelName + " speed to " + str(payload))
            handleSpeed(wheel, float(payload))
        if command == "cal":
            # wheel/<name>/cal/<command>/position
            topiclen = len(topicsplit)
            wheelCal = wheel["cal"]

            if topiclen < 4: # only cal
                m = "deg,90," + str(wheelCal["deg"]["90"]) + "\n"
                m = m + "deg,0," + str(wheelCal["deg"]["0"]) + "\n"
                m = m + "deg,-90," + str(wheelCal["deg"]["-90"]) + "\n"
                m = m + "speed,0," + str(wheelCal["speed"]["0"]) + "\n"
                m = m + "speed,300," + str(wheelCal["speed"]["300"]) + "\n"
                m = m + "speed,-300," + str(wheelCal["speed"]["-300"]) + "\n"
                client.publish("wheel/" + wheelName + "/cal/values", m)

            elif topiclen == 5: # calibration for position
                command = topicsplit[3]
                position = topicsplit[4]


                if DEBUG:
                    print("  Setting wheel " + wheelName + " calibration for " + command + "/" + position + " to " + str(int(payload)))

                if command == "deg" or  command == "speed" or command == "servo":
                    wheelCal[command][position] = int(payload)
                else:
                    wheelCal[command][position] = payload

                file = open("rover-calibration.config", 'wb')

                pickle.dump(storageMap, file, 0)

                file.close()
    else:
        print("ERROR: no wheel with name " +  wheelName + " fonund.")

def handleDeg(wheel, degrees):
    cal = wheel["cal"]["deg"]

    if degrees >= 0:
        servoPosition = interpolate(degrees / 90.0, cal["0"], cal["90"])
    else:
        servoPosition = interpolate((degrees + 90) / 90.0, cal["-90"], cal["0"])

    wheel["deg"] = degrees
    wheel["degsServoPos"] = servoPosition
    servoNumber = cal["servo"]

    moveServo(servoNumber, servoPosition)


def handleSpeed(wheel, speed):
    global storageMap

    cal = wheel["cal"]["speed"]

    if speed >= 0:
        servoPosition = interpolate(speed / 300, cal["0"], cal["300"])
    else:
        servoPosition = interpolate((speed + 300) / 300, cal["-300"], cal["0"])

    wheel["speed"] = speed
    wheel["speedServoPos"] = servoPosition
    servoNumber = cal["servo"]

    if str(speed) == "0":
        moveServo(servoNumber, servoPosition)


def interpolate(value, zero, max):
    return (max - zero) * value + zero

def driveWheel(wheelName):
    wheel = storageMap[wheelName]
    speed = wheel["speed"]
    if "speedServoPos" in wheel:
        servoPosition = wheel["speedServoPos"]

        cal = wheel["cal"]["speed"]
        servoNumber = cal["servo"]

        if str(speed) != "0":
            moveServo(servoNumber, servoPosition)

def driveWheels():
    driveWheel("fl")
    driveWheel("fr")
    driveWheel("bl")
    driveWheel("br")
