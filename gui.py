#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout

class MessengerWindow(GridLayout):
    def __init__(self, **kwargs):
        super(MessengerWindow, self).__init__(**kwargs)
        self.cols = 2
        self.username = (Label(text="Username: "))
        self.add_widget(self.username)
        self.chat_log = (Label(text="I am sending a message."))
        self.add_widget(self.chat_log)
        self.input_box = TextInput()
        self.add_widget(self.input_box)
        self.send = Button(text="TEST")
        self.send.bind(on_press=self.btn_pressed)
        self.add_widget(self.send)


    def btn_pressed(self, instance):
        print(self.input_box.text) 
        self.chat_log.text = self.input_box.text
        self.input_box.text=""
        

class MessengerApp(App):
    def build(self):
        return MessengerWindow()

MessengerApp().run()
