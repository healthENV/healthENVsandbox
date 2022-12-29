import socket
import json

def client_program(function, message):
    host = "launcher" #socket.gethostname()
    port = 5000  # socket server port number
    try:
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server
    except:
        print("Seems that launcher is not running")
        return
    else:
        toSend = {function, message}
        toSendJson = json.dumps(toSend)

        client_socket.send(toSendJson)  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print(data)
        client_socket.close()  # close the connection
        return data
