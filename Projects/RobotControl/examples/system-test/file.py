import os

whoami = os.popen("whoami")

line = 1
for line in whoami.readlines():
    # print("test: " + str(line) + ": " + line)
    print(line)
