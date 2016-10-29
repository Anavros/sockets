#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout

class MessengerWindow(GridLayout):
    def __init__(self, **kwargs):
        super(MessengerWindow, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Username: "))
        self.add_widget(Label(text="I am sending a message."))
        self.message = TextInput()
        self.add_widget(self.message)

class MessengerApp(App):
    def build(self):
        return MessengerWindow()

MessengerApp().run()
