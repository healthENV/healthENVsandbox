# app/ipc.py
 
"""Interprocess communication (IPC) - client end

Functions:
- client_program()
- sumOwn()

"""

import socket
import json

def client_program(function: str, user: str, env: str) -> str:
    """IPC (interprocess communication) with launcher container
        
        Examples:
            >>> client_program('up', 'user1', 'ENV1')
            Seems that launcher is not running
            '0'

        Args:
            function: docker-compose 'up' or 'down'
            user: user ID
            env: the ENV to use

        Returns:
            Message received from launcher container
    """

    host = "launcher" #socket.gethostname()
    port = 5000  # socket server port number
    try:
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server
    except:
        print("Seems that launcher is not running")
        return '0'
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