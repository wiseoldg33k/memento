from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class ContactAddWidget(StackLayout):
    def __init__(self, state, sm, **kwargs):
        self.state = state
        self.sm = sm
        super().__init__(**kwargs)

        self.name = TextInput(
            multiline=False,
            hint_text="Name",
            password=False,
            size_hint=(1, 0.2),
        )
        self.add_widget(self.name)

        self.add_button = Button(text="Add", size_hint=(1, 0.2))
        self.add_widget(self.add_button)
        self.add_button.bind(on_press=self.on_add_button_pressed)

    def on_add_button_pressed(self, instance):
        self.state.add_contact(name=self.name.text)
        self.state.dump()
        self.sm.current = "roster_screen"
