from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock


class CreateDBWidget(GridLayout):

    def __init__(self, state, db_filename, **kwargs):
        self.state = state
        self.db_filename = db_filename
        super().__init__(**kwargs)

        self.rows = 3
        self.add_widget(Label(text='Create New Database', font_size='70sp'))
        self.pincode = TextInput(multiline=False, font_size='70sp', 
                                 hint_text='Enter a PIN Code', password=False)
        self.add_widget(self.pincode)

        self.create_button = Button(text='Create', font_size='70sp')
        self.add_widget(self.create_button)        
        self.create_button.bind(on_press=self.on_create_button_pressed)

        Clock.schedule_once(self.show_keyboard, 0.2)

    def show_keyboard(self, _):
        self.pincode.focus = True

    def on_create_button_pressed(self, instance):
        Clock.schedule_once(self.create_db, 0.5)

    def create_db(self, _):
        key = self.state.hash_pin(self.pincode.text)
        self.state.dump(key, self.db_filename)

