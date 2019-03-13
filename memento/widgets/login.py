import cryptography

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class LoginWidget(GridLayout):

    def __init__(self, state, db_filename, sm, **kwargs):
        self.state = state
        self.db_filename = db_filename
        self.sm = sm
        super().__init__(**kwargs)

        self.rows = 3
        self.add_widget(Label(text='Memento', font_size='70sp'))
        self.pincode = TextInput(multiline=False, font_size='70sp', 
                                 hint_text='Enter a PIN Code', password=False)
        self.add_widget(self.pincode)

        self.login_button = Button(text='OK', font_size='70sp')
        self.add_widget(self.login_button)        
        self.login_button.bind(on_press=self.on_login_button_pressed)

        Clock.schedule_once(self.show_keyboard, 0.2)

    def show_keyboard(self, _):
        self.pincode.focus = True

    def on_login_button_pressed(self, instance):
        Clock.schedule_once(self.open_db, 0.5)

    def open_db(self, _):
        key = self.state.hash_pin(self.pincode.text)
        try:
            self.state.load(key, self.db_filename)
            self.sm.current = 'roster_screen'
        except cryptography.fernet.InvalidToken:
            close_button = Button(text='Close')
            popup = Popup(title='Invalid PIN code', 
                          content=close_button, 
                          size_hint=(.8, .2),
                          auto_dismiss=False)

            close_button.bind(on_press=popup.dismiss)

            popup.open()

