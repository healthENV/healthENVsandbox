import socket

def client_program():
    host = "launcher" #socket.gethostname()
    port = 5000  # socket server port number
    try:
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server
    except:
        print("Seems that launcher is not running")
        return
    else:
        message = "launch"

        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print(data)
        client_socket.close()  # close the connection
        return
