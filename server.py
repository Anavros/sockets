
import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from time import sleep

import malt

from constants import PORT, BUF_SIZE


def start_session():
    server = Server()
    server.start()
    try:
        server.loop()
    except KeyboardInterrupt:
        print(" Halting server due to keyboard interrupt...")
    server.stop()


class Server:
    """
    A simple echo server. Connects to one client at a time.
    """
    def __init__(self):
        self.host = ''
        self.socket = None
        self.selector = DefaultSelector()
        self.running = False
        self.users = {}
        self.log = []

    def start(self):
        """
        Open a socket at this server's host and port and begin listening.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, PORT))
        self.socket.listen(5)
        # Callback self.connect() when a client connects to the server.
        self.selector.register(self.socket, EVENT_READ)
        self.running = True

    def stop(self):
        """
        Close this server's socket.
        """
        self.running = False
        self.socket.close()

    def connect(self, server):
        client, addr = server.accept()
        user = User(addr)
        self.users[client] = User(addr)
        self.selector.register(client, EVENT_READ)
        print("Received connection from client at {}.".format(str(user)))

    def disconnect(self, s):
        name = str(self.users[s])
        del self.users[s]
        s.close()
        self.selector.unregister(s)
        print("Client at {} has disconnected.".format(name))

    def loop(self, timeout=0.0):
        while True:
            self.select(timeout)
            self.flush_messages()
            sleep(0.1)

    def select(self, timeout):
        for key, mask in self.selector.select(timeout):
            socket = key.fileobj
            if socket == self.socket:  # server message, client connecting.
                self.connect(socket)
            elif socket in self.users.keys():  # user message
                self.receive_message(socket)
            else:
                malt.log("Unknown selector event? {}".format(socket))

    def flush_messages(self):
        for socket, user in self.users.items():
            if user.pending:
                malt.log("Sending messages to {}.".format(user.name))
                socket.sendall('\0'.join(user.pending).encode())
                user.pending = []

    def receive_message(self, socket):
        user = self.users[socket]
        # Throws IOError when client disconnects.
        message = socket.recv(BUF_SIZE).decode()
        if message == '':  # Empty message indicates closed socket.
            self.disconnect(socket)
        else:
            try:
                head, tail = decode_message(message)
            except ValueError:
                return
            if head == 'name':
                # TODO: Add a notification message for name change
                malt.log("Renaming {} to {}.".format(str(user), tail))
                user.name = tail
            elif head == 'message':
                self.record(user, tail)
                malt.log("{}: '{}'.".format(user.name, tail))
            elif head == 'read':
                malt.log("Reading messages to {}.".format(user.name))
                socket.sendall('\0'.join(user.pending).encode())
                user.pending = []

    def record(self, user, message):
        text = user.name+': '+message
        self.log.append(message)
        for other in self.users.values():
            if other != user:
                other.pending.append(message)


class User:
    def __init__(self, address):
        ip, port = address
        self.address = ip
        PORT = port
        self.name = None
        self.pending = []

    def __str__(self):
        return "{}:{}".format(self.address, PORT)


def decode_message(message):
    if ':' not in message:
        raise ValueError("Message does not contain header.")
    head, tail = message.split(':', 1)
    return head, tail
