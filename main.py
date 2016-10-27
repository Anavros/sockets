
"""
Basic networking tests. Send messages from one computer to another.
"""

import socket
import malt
from sys import argv

from client import Client
from server import Server

PORT = 50002
BUF_SIZE = 1024
IP_HISTORY = "ip_history"
NAME_HISTORY = "name_history"


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
        username = get_username()
        address = get_address()
        print("Starting client session targeting address {} on port {}..."\
            .format(address, PORT))
        start_client_session(Client(username, address, PORT, BUF_SIZE))
        print("Client session ended.")

    elif side == 'server':
        print("Starting server on port {}...".format(PORT))
        start_server_session(Server(PORT, BUF_SIZE))
        print("Server process ended.")

    # If the second argument is not either 'client' or 'server':
    else: raise ValueError("Side must be either client or server.")


def start_client_session(client):
    client.connect()
    client.send(client.username, header = "name")
    options = [
        "msg s:message",
        "name s:name",
        "read"
    ]
    while True:
        response = malt.offer(options)
        if response.head == "msg":
            echo = client.send(response.message)
            print(echo)
        elif response.head == "name":
            client.send(response.name, header = "name")
            pass
        elif response.head == "read":
            client.send("msg", header = "read")
            new_messages = client.check_messages(timeout = 1.0)
            for message in new_messages:
                print(message)
    client.disconnect()

def start_server_session(server):
    server.start()
    try:
        server.loop()
    except KeyboardInterrupt:
        print(" Halting server due to keyboard interrupt...")
    server.stop()


def get_username():
    name_history = get_last_name()
    username = input("Enter your username (enter to use {}): ".format(name_history))
    if username == "":
        if name_history == "":
            username = "Anon"
        else:
            username = name_history
    else:
        write_name(username)
    return username

def get_address():
    ip_history = get_last_ip()
    address = input("Input IP address (enter to use {}): ".format(ip_history))
    if not address:
        return ip_history
    if address == 'localhost' or ip_check(address):
        write_ip(address)
        return address
    else:
        print("Invalid IP Address.")
        raise SystemExit  # hacky

def get_last_name():
    with open(NAME_HISTORY, "r") as f:
        name = f.read()
    return name

def write_name(name):
    with open(NAME_HISTORY, "w") as f:
        name = f.write(name)


def get_last_ip():
    """
    Read the last-used ip address from the history file.
    Returns a string which can be directly used as a host name.
    """
    with open(IP_HISTORY, "r") as f:
        ip = f.read()
    return ip


def write_ip(ip):
    """
    Overwrite the history file with the given ip address.
    Only one address, the most recently used, will be in the file at any time.
    """
    with open(IP_HISTORY, "w") as f:
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
