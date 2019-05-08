from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from ..backend import Backend


class LoginWidget(StackLayout):
    def __init__(self, state, db_filename, sm, **kwargs):
        self.state = state
        self.db_filename = db_filename
        self.sm = sm
        super().__init__(**kwargs)

        self.add_widget(Label(text="M", font_size="70sp", size_hint=(1, 0.6)))
        self.pincode = TextInput(
            multiline=False,
            hint_text="Enter a PIN Code",
            password=False,
            size_hint=(1, 0.1),
        )
        self.add_widget(self.pincode)

        self.login_button = Button(text="OK", size_hint=(1, 0.3))
        self.add_widget(self.login_button)
        self.login_button.bind(on_press=self.on_login_button_pressed)

        Clock.schedule_once(self.show_keyboard, 0.2)

    def show_keyboard(self, _):
        self.pincode.focus = True

    def on_login_button_pressed(self, instance):
        Clock.schedule_once(self.open_db, 0.5)

    def open_db(self, _):
        key = self.state.hash_pin(self.pincode.text)
        backend = Backend(db_location=self.db_filename, key=key)
        if backend.verify():
            self.state.set_backend(backend=backend)
            self.sm.current = "roster_screen"
        else:
            close_button = Button(text="Close")
            popup = Popup(
                title="Invalid PIN code",
                content=close_button,
                size_hint=(0.8, 0.2),
                auto_dismiss=False,
            )

            close_button.bind(on_press=popup.dismiss)

            popup.open()
