
"""
Basic networking tests. Send messages from one computer to another.
"""

import socket

PORT = 50002
BUF_SIZE = 1024
MESSAGE = 'Hello!'


def main(side):
    """
    Networking tests using sockets.
    >>> bool('Using doctests?')
    True
    """
    if side == 'client':
        Client().fire()
    elif side == 'server':
        Server().start()
    else:
        raise ValueError("Side must be either client or server.")


class Client:
    def __init__(self):
        self.host = 'localhost'
        self.port = PORT
        self.socket = None

    def fire(self):
        print('Sending message: "{}".'.format(MESSAGE))
        # AF_INET == internet/ipv4, SOCK_STREAM == TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.send(MESSAGE.encode())
        data = self.socket.recv(BUF_SIZE).decode()
        self.socket.close()
        print('Recieved response: "{}".'.format(data))


class Server:
    def __init__(self):
        self.host = ''
        self.port = PORT
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(4)  # backlog
        running = True
        while running:
            try:
                client, address = self.socket.accept()
                data = client.recv(BUF_SIZE)
                if data:
                    # the echo
                    client.send(data.upper())
            except (KeyboardInterrupt, OSError) as e:
                print("Error: ", e)
                running = False
            finally:
                client.close()


if __name__ == '__main__':
    from sys import argv
    if len(argv) != 2 or argv[1] not in ['client', 'server']:
        print("Usage: run <client|server>")
    else:
        side = argv[1]
        main(side)
