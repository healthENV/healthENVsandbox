#!/usr/bin/python3

import threading
import time as t
import socket
import docker
import os


exitFlag = [0]

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
    global exitFlag
    while exitFlag[0] == 0:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            print("from connected user: " + str(data))
            if data == "launch":
                print("launching")
                os.chdir("/dockerfiles/ENV2")
                os.system('docker-compose up')
            returnMessage = "Received and acted upon"
            conn.send(returnMessage.encode())  # send data to the client

        conn.close()  # close the connection
    return


if __name__ == '__main__':
	# Create new threads and start
	ipcComm = ipcClass()
	ipcComm.start()