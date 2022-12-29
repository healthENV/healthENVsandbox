#!/usr/bin/python3

import threading
import time as t
import socket
import os
import signal
from datetime import datetime
import sys
import json

exitFlag = [0]
#print(f"exit flag is: { exitFlag[0]}")

logFile = "/logs/launcher.txt"


runningENVs = []
mainEnvLocation = "/dockerfiles/"


def logMsg(message):
    now = datetime.now()
    dateTime = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"{ dateTime } - { message }")
    f = open(logFile, "a")
    f.write(f"{ dateTime } - { message }\n")
    f.close()

logMsg("Launcher start up")


def handler_stop_signals(signum, frame):
    global runningENVs, exitFlag
    logMsg("Closing down routine...")

    while len(runningENVs) != 0:
        location = runningENVs.pop()
        os.chdir(location)
        logMsg(f"Closing containers at: { location }")
        os.system('docker-compose down')
    #print(f"exit flag is: { exitFlag[0] }")
    exitFlag[0] = 1
    #print(f"exit flag is: { exitFlag[0] }")
    sys.exit(0)


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)



# Threading code for Django to python communication
class ipcClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        # get the hostname
        host = socket.gethostname()
        port = 5000  # initiate port no above 1024

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many client the server can listen simultaneously
        server_socket.listen(2)
        print("now listening out for clients")
        ipcThread(server_socket)
        print('Exited thread and class')	


def ipcThread(server_socket):
    global exitFlag, runningENVs

    #print(f"exit flag is: { exitFlag[0] }")
    while exitFlag[0] == 0:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))

        while exitFlag[0] == 0:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            receivedMsgJson = conn.recv(1024).decode()
            
            if not receivedMsgJson:
                # if data is not received break
                break

            receivedMsg = json.loads(receivedMsgJson)
            print("Message from portal: " + str(receivedMsg))
            logMsg(f"Message from portal: { receivedMsg }")
            if receivedMsg[0] == "up":
                print(f'Launching { receivedMsg[2] }...')
                envLocation = f'{ mainEnvLocation }/{ receivedMsg[1]}/{ receivedMsg[2] }'
                os.chdir(envLocation)
                os.system('docker-compose up -d')
                runningENVs.append(envLocation)
                returnMessage = f'Containers in "{ receivedMsg[2] }" are starting up...'
            elif receivedMsg[0] == "down":
                # Need to test if is actually running
                print(f'Stopping { receivedMsg[2] }...')
                envLocation = f'{ mainEnvLocation }/{ receivedMsg[1]}/{ receivedMsg[2] }'
                os.chdir(envLocation)
                os.system('docker-compose down')
                runningENVs.remove(envLocation)
                returnMessage = f'Containers in "{ receivedMsg[2] }" have been stopped'
            else:
                returnMessage = "Message acknowledged (but no function called)"
            conn.send(returnMessage.encode())  # send data to the client

        conn.close()  # close the connection
    #print(f"exit flag is: { exitFlag[0] }")
    return


if __name__ == '__main__':
	# Create new threads and start
	ipcComm = ipcClass()
	ipcComm.start()