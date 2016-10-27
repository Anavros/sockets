
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

        self.client = None
        self.client_address = None
        self.connected = False

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
                # Accept a new incoming connection.
                client, addr = i.accept()
                self.users.append(User(client, addr))
                print("Received connection from client at {}.".format(addr))
            else:
                # Received a message from a client.
                message = i.recv(self.buf_size).decode()
                print("Received message: '{}'.".format(message))

    def stop(self):
        """
        Close this server's socket.
        """
        self.running = False
        self.socket.close()

    def wait_for_client(self):
        """
        Wait for an incoming connection. Stores the client socket and address
        as member variables.
        """
        self.client, self.client_address = self.socket.accept()
        name = "Nobody"
        self.users[name] = User(self.client, self.client_address, name)
        self.connected = True
        self.current_user = name

    def disconnect(self):
        """
        Close the client socket and reset vars to None.
        """
        self.connected = False
        self.client.close()
        self.client = None
        self.client_address = None

    def wait_for_message(self):
        """
        Wait for and return a message from a connected client.
        Server must be running and connected to a client. Throws IOError if not.
        """
        if not self.running:
            raise IOError("Server must be running to receive messages!")
        if not self.connected:
            raise IOError(
                "Server must be connected to a client to receive messages!")
        return self.client.recv(self.buf_size).decode()

    def send(self, message):
        """
        Send a message to a connected client.
        Server must be running and connected to a client. Throws IOError if not.
        """
        if not self.running:
            raise IOError("Server must be running to send messages!")
        if not self.connected:
            raise IOError(
                "Server must be connected to a client to send messages!")
        self.client.sendall(message.encode())


class User:
    def __init__(self, socket, address, username='None'):
        self.socket = socket
        ip, port = address
        self.address = ip
        self.port = port
        self.username = username
        self.connected = False
