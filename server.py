
import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

class Server:
    """
    A simple echo server. Connects to one client at a time.
    """
    def __init__(self, port, buf_size):
        self.host = ''
        self.port = port
        self.buf_size = buf_size
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
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        # Callback self.connect() when a client connects to the server.
        self.selector.register(self.socket, EVENT_READ, self.connect)
        self.running = True

    def loop(self, timeout=60.0):
        while True:
            for key, mask in self.selector.select(timeout):
                fun = key.data
                fun(key.fileobj)

    def receive_message(self, socket):
        user = self.users[socket]
        message = socket.recv(self.buf_size).decode()
        if message == '':  # Empty message indicates closed socket.
            self.disconnect(socket)
        else:
            if user.name is None:
                user.name = message
            else:
                print("{}: '{}'.".format(user.name, message))
                socket.sendall(message.encode())

    def connect(self, server):
        client, addr = server.accept()
        user = User(addr)
        self.users[client] = User(addr)
        self.selector.register(client, EVENT_READ, self.receive_message)
        print("Received connection from client at {}.".format(str(user)))

    def disconnect(self, s):
        name = str(self.users[s])
        del self.users[s]
        s.close()
        self.selector.unregister(s)
        print("Client at {} has disconnected.".format(name))

    def stop(self):
        """
        Close this server's socket.
        """
        self.running = False
        self.socket.close()


class User:
    def __init__(self, address):
        ip, port = address
        self.address = ip
        self.port = port
        self.name = None
        self.pending = []

    def __str__(self):
        return "{}:{}".format(self.address, self.port)
