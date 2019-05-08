from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from . import use_font
from memento.backend import Backend


class CreateDBWidget(StackLayout):
    def __init__(self, state, db_filename, **kwargs):
        self.state = state
        self.db_filename = db_filename
        super().__init__(**kwargs)

        self.add_widget(Label(text="M", font_size="70sp", size_hint=(1, 0.6)))
        self.add_widget(
            Label(
                markup=True,
                text=use_font(
                    """
No database found

1. Enter a PIN code
2. Press Create
                """
                ),
                size_hint=(1, 0.2),
            )
        )
        self.pincode = TextInput(
            multiline=False,
            hint_text="Enter a PIN Code",
            password=False,
            size_hint=(1, 0.1),
        )
        self.add_widget(self.pincode)

        self.create_button = Button(text="Create", size_hint=(1, 0.1))
        self.add_widget(self.create_button)
        self.create_button.bind(on_press=self.on_create_button_pressed)

        Clock.schedule_once(self.show_keyboard, 0.2)

    def show_keyboard(self, _):
        self.pincode.focus = True

    def on_create_button_pressed(self, instance):
        Clock.schedule_once(self.create_db, 0.5)

    def create_db(self, _):
        key = self.state.hash_pin(self.pincode.text)
        backend = Backend(db_location=self.db_filename, key=key)
        backend.init()
