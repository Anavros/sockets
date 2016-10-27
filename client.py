
import socket

class Client:
    """
    A simple client which connects to one server and can send any number of
    simple messages before closing.
    """
    def __init__(self, username, address, port, buf_size):
        self.username = username
        self.host = address
        self.port = port
        self.buf_size = buf_size
        self.socket = None
        self.connected = False

    def connect(self):
        """
        Connect to a given host and port.
        Meant for long-term connections.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))  # probably throws errors
        self.connected = True
        response = self.exchange(self.username)

    def disconnect(self):
        """
        Close this client's socket.
        """
        self.connected = False
        self.socket.close()

    def exchange(self, message):
        """
        Send a message to the connected server.
        Must already be connected before sending messages.
        Returns decoded strings received from the server.
        """
        if not self.connected: raise IOError(
            "Client must be connected to a server before sending messages!")
        # A little hacky. If the user enters nothing, it will stall the program.
        # There's probably a better way to handle this, but it will work for now.
        if not message: return ''
        self.socket.sendall(message.encode())
        received = self.socket.recv(self.buf_size).decode()
        return received

    def test_connection():
        """
        Send a probe packet to the server to ensure the connection works.
        """
        pass
