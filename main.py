
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
        address = input("Input IP Address: ")
        while True:
            new_message = input("Enter a message to send the server or ctrl+c to quit: ")
            Client(address).fire(new_message)
    elif side == 'server':
        Server().start()
    else:
        raise ValueError("Side must be either client or server.")


class Client:
    def __init__(self, address):
        self.host = address
        self.port = PORT
        self.socket = None

    def fire(self, new_message):
        print('Sending message: "{}".'.format(new_message))
        # AF_INET == internet/ipv4, SOCK_STREAM == TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.send(new_message.encode())
        data = self.socket.recv(BUF_SIZE).decode()
        self.socket.close()
        print('Recieved response: "{}".'.format(data))


class Server:
    def __init__(self):
        self.host = ''
        self.port = PORT
        self.socket = None
        self.message_count = 0

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
                    self.message_count += 1
                    client.send(self.gen_message(data, self.message_count))
            except OSError as e:
                print("OSError: ", e)
                running = False
            except KeyboardInterrupt:
                print("Halting server.")
                running = False
            finally:
                client.close()

    def gen_message(self, data, n):
        return "{}\nYou have sent {} messages over this server's lifetime."\
            .format(data, n).encode()


if __name__ == '__main__':
    from sys import argv
    # ./run client [ip address]
    if len(argv) != 2:
        print("The length of the argument is incorrect")
    elif argv[1] not in ['client', 'server']:
        print("Usage: run <client|server>")
    else:
        side = argv[1]
        main(side)







