#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from backend import Backend

class MessengerWindow(FloatLayout):
    def __init__(self, **kwargs):
        super(MessengerWindow, self).__init__(size=(500, 300),**kwargs)
        self.backend = Backend()
        self.cols = 2
        self.username = (Label(text="Username: ",size_hint=(.1, .3), pos =(10,490)))
        self.add_widget(self.username)
        self.chat_log = (Label(text="", size_hint=(.1, .3), pos =(100,490)))
        self.add_widget(self.chat_log)
        self.input_box = TextInput(size_hint=(.7, .5), pos=(220,10), multiline=False)
        self.add_widget(self.input_box)
        self.send = Button(text="Send", size_hint=(.25, .5), pos=(10,10))
        self.send.bind(on_press=self.btn_pressed)
        self.add_widget(self.send)

    def btn_pressed(self, instance):
        print(self.input_box.text) 
        self.backend.send(self.input_box.text)
        self.input_box.text=""
        

class MessengerApp(App):
    def build(self):
        return MessengerWindow()

if __name__ == "__main__":
    MessengerApp().run()
