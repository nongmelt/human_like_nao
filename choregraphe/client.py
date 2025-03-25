import socket
import random
import time

#host = '169.254.13.207'
host = '127.0.0.1'
port = 8888

client_socket = None

class MyClass(GeneratedClass):

    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        # Called when "play" is pressed
        pass

    def onInput_onStart(self):

        ### 1. Define the server
        self.logger.info("Connecting to socket...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.logger.info("Connecting to server...")
        msgs = ""
        try:
            client_socket.connect((host, port))
            client_socket.sendall("emit:connect".encode())
            raw_msgs = client_socket.recv(1024).decode()
            msgs = ""
            msgs += str(raw_msgs)
            self.logger.info(msgs)
            client_socket.sendall("emit:disconnect".encode())
        except Exception as err:
            self.logger.error(err)

        self.onStopped(msgs)
        pass

    def onInput_onStop(self):
        self.onUnload()

    def onUnload(self):
        # Close the socket when stopped
        if client_socket is not None:
            client_socket.close()
