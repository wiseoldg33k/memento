import os

from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class ImageButton(ButtonBehavior, Image):
    def __init__(self, source, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.source = source


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

        self.layout = GridLayout(
            cols=3,
            spacing=5,
            padding=(5, 5, 5, 5),
            row_force_default=True,
            size_hint_y=None,
            row_default_height=200,
        )

        self.layout.bind(minimum_height=self.layout.setter("height"))

        scroll = ScrollView(size_hint=(1, 0.8))
        scroll.add_widget(self.layout)

        self.add_widget(scroll)

        self.loaded = {}

    def on_pre_enter(self, *args, **kwargs):
        print("found {} contacts".format(len(self.state.list_contacts())))
        for contact in sorted(
            self.state.list_contacts(), key=lambda x: x.name
        ):
            print("contact:", contact.name)
            if contact.name not in self.loaded:

                if contact.profile_picture and os.path.isfile(
                    contact.profile_picture
                ):
                    btn = ImageButton(source=contact.profile_picture)
                else:
                    btn = Button(text=contact.name)
                self.loaded[contact.name] = btn
                self.layout.add_widget(btn)

    def on_add_button_pressed(self, instance):
        self.sm.current = "contact_add_screen"
