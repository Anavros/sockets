
import socket
from contextlib import contextmanager

class Server:
    def __init__(self, port, buf_size):
        self.host = ''
        self.port = port
        self.buf_size = buf_size
        self.socket = None
        self.running = False
        self.client = None
        self.client_address = None
        self.connected = False

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(4)  # allow four pending connections
        self.running = True

    def stop(self):
        self.running = False
        self.socket.close()

    def wait_for_client(self):
        self.client, self.client_address = self.socket.accept()
        self.connected = True

    def disconnect(self):
        self.connected = False
        self.client.close()
        self.client = None
        self.client_address = None

    def wait_for_message(self):
        if not self.running:
            raise IOError("Server must be running to receive messages!")
        if not self.connected:
            raise IOError("Server must be connected to a client to receive messages!")
        return self.client.recv(self.buf_size).decode()

    def send(self, message):
        if not self.running:
            raise IOError("Server must be running to send messages!")
        if not self.connected:
            raise IOError("Server must be connected to a client to send messages!")
        self.client.send(message.encode())


class User:
    # address, port, socket, and username
    pass
