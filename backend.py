
"""
Wrapper layer for the GUI to interact with a client.
"""

import malt

from client import Client
from constants import USER_PATH


def get_gui_backend():
    """
    Create a return a new client, using saved username and address.
    """
    return Client(*load_user())


def load_user():
    users = malt.load(USER_PATH)
    u = users[0]  # just use the first one for now
    return u.name, u.address
