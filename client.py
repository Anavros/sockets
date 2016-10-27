
import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

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
        self.selector = DefaultSelector()
        self.messages = []

    def connect(self):
        """
        Connect to a given host and port.
        Meant for long-term connections.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))  # probably throws errors
        self.selector.register(self.socket, EVENT_READ)
        self.connected = True

    def disconnect(self):
        """
        Close this client's socket.
        """
        self.connected = False
        self.socket.close()

    def exchange(self, message, header='message', wait_for_return=False):
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
        self.socket.sendall((header+':'+message).encode())
        if wait_for_return:
            received = self.socket.recv(self.buf_size).decode()
            return received
        else:
            return ''

    def send(self, message, header='message'):
        self.exchange(message, header, wait_for_return=False)

    def check_messages(self, timeout=0.0):
        messages = []
        for key, mask in self.selector.select(timeout):
            socket = key.fileobj
            message = socket.recv(self.buf_size)
            messages.append(message.decode())
        return messages

    def test_connection():
        """
        Send a probe packet to the server to ensure the connection works.
        """
        pass
