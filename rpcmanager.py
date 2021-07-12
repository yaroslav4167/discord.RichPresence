import random
import time

import pyautogui
from pypresence import Presence


class RPCManager(Presence):

    def __init__(self, app_id=None):
        if app_id is None:
            self.app_id = 123456789123456789
        else:
            self.app_id = app_id
        self.connected = False
        # self.RPC = None
        super(RPCManager, self).__init__(self.app_id)

    def set_app_id(self, app_id):
        self.app_id = app_id

    def connect(self, app_id=None):
        if app_id is not None:
            self.set_app_id(app_id)
        if self.connected:
            return "RPC already connected!"
        try:
            # self.RPC = Presence(self.app_id) # Initialize the Presence class
            # self.RPC.connect()
            self.client_id = self.app_id
            super().connect()
        except TimeoutError:
            return "Token error!"
        finally:
            self.connected = True
            return "Connected!"

    def disconnect(self):
        if not self.connected:
            return "RPC is not connected!"
        self.close()
        self.connected = False
        return "RPC disconnected!"
