import socketserver
import threading
from typing import Literal
from loguru import logger
from collections import deque

HOST, PORT = "0.0.0.0", 8888

class TCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.server_instance = kwargs.pop('server_instance')
        super().__init__(*args, **kwargs)

    def handle(self):
        logger.info("Client connected: {}", self.client_address)
        data = self.request.recv(1024).strip()
        logger.info("Received: {}", data.decode('utf-8'))

        if len(self.server_instance.messages_queue) != 0:
            try:
                payload = self.server_instance.messages_queue.popleft()
                self.request.sendall(payload.encode("utf-8"))
                logger.info("Sent message to client: {}", payload)
            except Exception as e:
                logger.error("Error sending message to client: {}", e)


class Server:
    def __init__(self, mode: Literal["robot", "human"], host=HOST, port=PORT):
        self.server = socketserver.TCPServer(
            (host, port),
            lambda *args, **kwargs: TCPHandler(*args, **kwargs, server_instance=self))
        self.mode = mode
        self.client_socket = None
        self.messages_queue = deque()
        logger.info("Server started on port {}", port)

        self.thr = threading.Thread(target=self.server.serve_forever)
        self.running = False

    def start(self):
        self.thr.start()
        self.running = True

    def stop(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except Exception as e:
                logger.error("Error closing client connection: {}", e)
        self.server.shutdown()
        self.server.server_close()
        logger.info("Server closed")
    def set_client_socket(self, client_socket):
        self.client_socket = client_socket
        logger.info("Client socket set: {}", self.client_socket)

    def send(self, message: str):
        self.messages_queue.append(f"{self.mode}:{message}")
