"""
    Interprocess communication (IPC) - client end
"""

import socket
import json

def client_program(function, user, env):
    """IPC (interprocess communication) with launcher container

        :param str function: docker-compose 'up' or 'down'
        :param str user: user ID
        :param str env: the ENV to use

        :returns: Message received from launcher container

        :rtype: str or int
    """

    host = "launcher" #socket.gethostname()
    port = 5000  # socket server port number
    try:
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server
    except:
        print("Seems that launcher is not running")
        return 0
    else:
        toSend = [function, user, env]
        toSendJson = json.dumps(toSend)

        client_socket.send(toSendJson.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print(data)
        client_socket.close()  # close the connection
        return data


def sumOwn(arg):
    """ Test sum method
    
    """
    total = 0
    for val in arg:
        total += val
    return total