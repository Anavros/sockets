
"""
Basic networking tests. Send messages from one computer to another.
"""

import socket
from sys import argv

import client
import server
from constants import PORT, BUF_SIZE, IP_HISTORY, NAME_HISTORY

def main():
    """
    Networking tests using sockets.
    """
    side = get_side()
    if side == 'gui':
        run_gui_client()
    elif side == 'server':
        run_server()
    elif side == 'client':
        run_client()


def get_side():
    """Parse argv and return network side of current session."""
    side = argv[1]
    if side in ['client', 'server', 'gui']:
        return side
    else:
        print("Usage: ./run <client|server|gui>")
        raise SystemExit


def run_client():
    username = get_username()
    address = get_address()
    print("Starting client session targeting address {} on port {}..."\
        .format(address, PORT))
    client.start_session(username, address)
    print("Client session ended.")


def run_gui_client():
    # only import Kivy if using GUI, otherwise tons of log spam
    from gui import MessengerApp
    app = MessengerApp()
    app.run()


def run_server():
    print("Starting server on port {}...".format(PORT))
    server.start_session()
    print("Server process ended.")


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
