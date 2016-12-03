import socket
import threading
import multiprocessing

global running

running = True

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket._LOCALHOST, 6321))
serversocket.listen(5)
serversocket.settimeout(0.5)

def clientThread(socket):
    global running

    try:
        print("Got connection!")
        socketfile = socket.makefile("rw")

        line = socketfile.readline().rstrip("\n")
        print("Received: '" + line + "'")

        socketfile.write("Hello!\n")
        socketfile.write("You sent: " + line)
        socketfile.write("Now we end\n")
        if "stop" == line:
            running = False
            print("In client thread - stopping")
    finally:
        socket.close()


def startThread(clientsocket):
    thread = threading.Thread(None, clientThread, None, [clientsocket])
    thread.daemon = True
    thread.start()

    # process = multiprocessing.Process(None, clientThread, None, [clientsocket])
    # process.start()


def accept():
    try:
        (clientsocket, address) = serversocket.accept()
        startThread(clientsocket)
    except socket.timeout:
        pass

try:

    print("Starting loop")
    while running:
        accept()
        print("Next loop...")

finally:
    print("Stopping!")
    serversocket.close()