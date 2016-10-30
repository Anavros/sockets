
"""
Wrapper layer for the GUI to interact with a client.
"""

import malt
from kivy.clock import Clock
from client import Client
from constants import USER_FILE


#Example:
"""
class MessengerApp:
    def __init__(self):
        self.button = Button(callback=self.msg)
        self.textentry = TextEntry()
        self.display = Label()
        self.backend = Backend()

    def msg():
        self.backend.send(self.textentry.text)
        self.textentry.text = ''
"""

class Backend:
    def __init__(self):
        Clock.schedule_interval(self.read, 1.0)
        self.username, self.host = load_user()
        self.client = Client(self.username, self.host)
        self.client.connect()
        self.client.send(self.username, header = "name")

    def read(self, dt):
        if self.client.new_messages():
            for m in self.client.get_messages():
                print("[SERVER] "+m)

    def send(self, message):
        self.client.send(message)


def load_user():
    users = malt.load(USER_FILE)
    u = users[0]  # just use the first one for now
    return u.name, u.address
