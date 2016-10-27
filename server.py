
import socket
import select

class Server:
    """
    A simple echo server. Connects to one client at a time.
    """
    def __init__(self, port, buf_size):
        self.host = ''
        self.port = port
        self.buf_size = buf_size
        self.socket = None
        self.running = False

        self.users = []
        self.log = []

    def start(self):
        """
        Open a socket at this server's host and port and begin listening.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.running = True

    def loop(self, timeout=60.0):
        while True:
            all_inputs = [self.socket] + [u.socket for u in self.users]
            ready_inputs, _, _ = select.select(all_inputs, [], [], timeout)
            self._read_inputs(ready_inputs)

    def _read_inputs(self, inputs):
        for i in inputs:
            if i == self.socket:
                self.connect(i)
            else:
                self.receive_message(i)

    def receive_message(self, sock):
        user = self.find_user_by_socket(sock)
        message = sock.recv(self.buf_size).decode()
        if message == '':
            # Empty message indicates closed socket.
            self.disconnect(user)
        else:
            if user.name is None:
                user.name = message
            else:
                print("{}: '{}'.".format(user.name, message))

    def connect(self, socket):
        client, addr = socket.accept()
        self.users.append(User(client, addr))
        print("Received connection from client at {}.".format(addr))

    def disconnect(self, user):
        user.socket.close()
        self.users.remove(user)
        print("Client at {} has disconnected.".format(user.address))

    def find_user_by_socket(self, socket):
        for user in self.users:
            if user.socket == socket:
                return user
        raise ValueError("Socket->User lookup failed!")

    def stop(self):
        """
        Close this server's socket.
        """
        self.running = False
        self.socket.close()


class User:
    def __init__(self, socket, address, name=None):
        self.socket = socket
        ip, port = address
        self.address = ip
        self.port = port
        self.name = name

    def __str__(self):
        return "{}@{}:{}".format(self.name, self.address, self.port)
