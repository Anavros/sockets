#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.config import Config
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
        Clock.schedule_interval(self.show_messages, 1.0)
        self.input_box = TextInput(size_hint=(.7, .5), pos=(220,10), multiline=False)
        self.add_widget(self.input_box)
        self.send = Button(text="Send", size_hint=(.25, .5), pos=(10,10))
        self.send.bind(on_press=self.btn_pressed)
        self.add_widget(self.send)

    def btn_pressed(self, instance):
        print(self.input_box.text)
        self.backend.send(self.input_box.text)
        self.input_box.text=""

    def show_messages(self, dt):
        messages = self.backend.read()
        for message in messages:
            self.chat_log.text += '\n' + message


class SimpleMessenger(GridLayout):
    """
    Basic, feature-stripped messenger client. Contains two panels: one for
    entering text, and another to display it.
    """
    def __init__(self, **kwargs):
        GridLayout.__init__(self, **kwargs)
        self.backend = Backend()
        self.rows = 2
        self.cols = 1
        # multiline=False means that the on_text_validate callback will fire
        # when the user presses enter within the field.
        self.entry = TextInput(multiline=False, on_text_validate=self.send)
        # Sizing the label is very non-intuitive. It's left-justified by
        # default, but that doesn't matter because the actual text in put into
        # a texture, just big enough to hold it, and then the *texture* is
        # rendered onto the screen, smack-dab in the middle.
        # So setting text_size to roughly the size of the panel is a temporary
        # workaround.
        self.label = Label(text_size=(395, 95))  # little hacky to hardcode
        self.add_widget(self.label)
        self.add_widget(self.entry)
        # Setting focus is also unnecessarily complex. To give something input
        # focus, you set focus=True, which auto-magically triggers some event
        # that requests keyboard focus. But it straight-up won't work if you
        # just call it directly. So you have to schedule it on the clock.
        Clock.schedule_once(self.focus)
        # And this is just the timer that fetches new messages from the server.
        Clock.schedule_interval(self.show, 1.0)

    # The '_' argument name here is just a normal name, like any other,
    # but it implies that we aren't going to do anything with it. So it's a
    # stylistic trick to get a variable and still show that it's not needed.
    def focus(self, _):
        """
        Focus the user's input into the text entry field. Has to be on
        a scheduled callback! Or else it won't do anything, for unknown reasons.
        """
        self.entry.focus = True

    def send(self, _):
        """
        Take text from the entry field and send it to the server. Clears
        the field afterwards.
        """
        self.backend.send(self.entry.text)
        self.entry.text = ""
        Clock.schedule_once(self.focus)  # keeps focus inside text input

    def show(self, _):
        """
        Append any new messages to the label. If there are no new messages,
        does nothing.
        """
        messages = self.backend.read()
        for message in messages:
            self.label.text += '\n' + message


class MessengerApp(App):
    def build(self):
        Config.set('graphics', 'width', 400)
        Config.set('graphics', 'height', 200)
        #return MessengerWindow()
        return SimpleMessenger()


if __name__ == "__main__":
    MessengerApp().run()
