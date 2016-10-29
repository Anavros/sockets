
import socket
from sys import stdin
from select import select
from constants import PORT, BUF_SIZE


def start_term_session(*args):
    start_session(*args)
def start_session(username, address):
    client = Client(username, address)
    client.connect()
    client.send(client.username, header = "name")
    while True:
        #print('tick', flush=True)
        if client.new_messages():
            #print("New messages!", flush=True)
            for msg in client.get_messages():
                if msg: print(msg, flush=True)
        if client.new_user_input():
            #print("User input is ready!", flush=True)
            text = client.get_user_input()
            client.send(text)
    client.disconnect()


# Callbacks for gui.
def get_message_log():
    pass


def send_message(message):
    pass


class Client:
    """
    A simple client which connects to one server and can send any number of
    messages before closing.
    """
    def __init__(self, username, address):
        self.username = username
        self.host = address
        self.socket = None
        self.connected = False
        self.errmsg = "Client must be connected to a server before communicating!"
        self.messages = []

    def connect(self):
        """
        Connect to a given host and port.
        Meant for long-term connections.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, PORT))  # probably throws errors
        self.connected = True

    def disconnect(self):
        """
        Close this client's socket.
        """
        self.connected = False
        self.socket.close()

    # if client.new_messages(): client.get_messages()
    def new_messages(self):
        """
        Perform a non-blocking check on either self.socket.
        Returns True if socket is ready for reading.
        """
        ready, _, _ = select([self.socket], [], [], 0.0)
        return self.socket in ready

    def get_messages(self):
        """
        Receive new messages from the server.
        Check if new_messages() before calling; this will block otherwise.
        """
        data = self.socket.recv(BUF_SIZE).decode()
        return data.split('\0')

    def new_user_input(self):
        """
        Returns True if the user has entered new input on STDIN.
        Calls to input() should not block when this returns True.
        """
        ready, _, _ = select([stdin], [], [], 0.0)
        return stdin in ready

    def get_user_input(self):
        return stdin.readline().strip()

    def send(self, message, header='message'):
        """
        Send a message with optional header to the connected server.
        """
        if not message: return
        self.socket.sendall((header+':'+message).encode())
