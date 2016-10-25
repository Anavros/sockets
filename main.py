
"""
Basic networking tests. Send messages from one computer to another.
"""

import socket
from sys import argv

from client import Client
from server import Server

PORT = 50002
BUF_SIZE = 1024
HISTORY = "history"


def main():
    """
    Networking tests using sockets.
    >>> bool('Using doctests?')
    True
    """
    # Moved startup/argument parsing code into main().
    usage_message = "Usage: run <client|server>"
    if len(argv) != 2:
        # Print usage and quit early if the wrong number of args is given.
        print(usage_message)
        return

    side = argv[1]
    if side == 'client':
        address = get_address_from_user()
        print("Starting client session targeting address {} on port {}..."\
            .format(address, PORT))
        start_client_session(Client(address, PORT, BUF_SIZE))
        print("Client session ended.")

    elif side == 'server':
        print("Starting server on port {}...".format(PORT))
        try:
            start_server_session(Server(PORT, BUF_SIZE))
        except KeyboardInterrupt:
            print(" Halting server due to keyboard interrupt...")
        print("Server process ended.")

    # If the second argument is not either 'client' or 'server':
    else: raise ValueError("Side must be either client or server.")


def start_client_session(client):
    client.connect()
    while True:
        try:
            new_message = input("Enter a message (ctrl+c to quit): ")
        except KeyboardInterrupt:
            print("\nExiting client.")
            break
        else:
            return_message = client.exchange(new_message)
            print(return_message)
    client.disconnect()

def start_server_session(server):
    server.start()
    while True:
        # Can handle multiple clients one at a time.
        server.wait_for_client()
        print("Received connection from client at {}.".format(server.client_address))
        while True:
            # KeyboardInterrupts will break this loop.
            # It's handled up one level, when this is called from main().
            message = server.wait_for_message()
            # If the client disconnects, the message will be an empty string.
            if message:
                print("Received message from client: '{}'".format(message))
                server.send(message.upper())
            else:
                print("Connection closed by client.")
                break
        print("Disconnecting client {}.".format(server.client_address))
        server.disconnect()
    server.stop()


def get_address_from_user():
    last_used = get_last_ip()
    address = input("Input IP Address (enter to use {}): ".format(last_used))
    if not address:
        return last_used
    if address == 'localhost' or ip_check(address):
        write_ip(address)
        return address
    else:
        print("Invalid IP Address.")
        raise SystemExit  # hacky


def get_last_ip():
    """
    Read the last-used ip address from the history file.
    Returns a string which can be directly used as a host name.
    """
    with open(HISTORY, "r") as f:
        ip = f.read()
    return ip


def write_ip(ip):
    """
    Overwrite the history file with the given ip address.
    Only one address, the most recently used, will be in the file at any time.
    """
    with open(HISTORY, "w") as f:
        f.write(ip)


def ip_check(ip):
    """
    This checks to make sure the IP is valid.
    >>> ip_check('blah')
    False
    >>> ip_check('192.168.1.76')
    True
    """
    try:
        socket.inet_aton(ip)
    except OSError:
        return False
    else:
        return True


if __name__ == '__main__':
    main()
