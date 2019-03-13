from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class RosterWidget(StackLayout):

    def __init__(self, state, sm, **kwargs):
        self.state = state
        self.sm = sm
        super().__init__(**kwargs)

        self.add_widget(Label(text='List Placeholder', 
                              font_size='70sp', 
                              size_hint=(1, .8),))

        self.add_button = Button(text='Add',
                                 font_size='70sp', 
                                 size_hint=(1, .2))
        self.add_widget(self.add_button)        
        self.add_button.bind(on_press=self.on_add_button_pressed)

    def on_add_button_pressed(self, instance):
        print('add button pressed')
