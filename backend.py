
"""
Wrapper layer for the GUI to interact with a client.
"""

import malt
from kivy.clock import Clock
from client import Client
from constants import USER_FILE


class Backend:
    def __init__(self):
        self.username, self.host = load_user()
        self.client = Client(self.username, self.host)
        self.client.connect()
        self.client.send(self.username, header = "name")

    def read(self):
        if self.client.new_messages():
            return self.client.get_messages()
        else:
            return []

    def send(self, message):
        self.client.send(message)


def load_user():
    users = malt.load(USER_FILE)
    u = users[0]  # just use the first one for now
    return u.name, u.address
