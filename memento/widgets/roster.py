from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class RosterWidget(StackLayout):
    def __init__(self, state, sm, **kwargs):
        self.state = state
        self.sm = sm
        super().__init__(**kwargs)

        self.add_button = Button(
            text="Add", font_size="70sp", size_hint=(1, 0.2)
        )
        self.add_widget(self.add_button)
        self.add_button.bind(on_press=self.on_add_button_pressed)

    def on_pre_enter(self, *args, **kwargs):
        # TODO: remove previous labels when adding new ones
        print("found {} contacts".format(len(self.state.list_contacts())))
        for contact in self.state.list_contacts():

            print("contact:", contact.name)

            self.add_widget(
                Label(text=contact.name, font_size="50sp", size_hint=(1, 0.1))
            )

    def on_add_button_pressed(self, instance):
        self.sm.current = "contact_add_screen"