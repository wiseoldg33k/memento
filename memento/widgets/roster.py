from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


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

        self.layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        scroll = ScrollView(
            size_hint=(1, None), size=(Window.width, Window.height)
        )
        scroll.add_widget(self.layout)

        self.add_widget(scroll)

        self.loaded = {}

    def on_pre_enter(self, *args, **kwargs):
        # TODO: remove previous labels when adding new ones
        print("found {} contacts".format(len(self.state.list_contacts())))
        for contact in self.state.list_contacts():
            print("contact:", contact.name)
            if contact.name not in self.loaded:
                btn = Button(text=contact.name, font_size="50sp")
                self.loaded[contact.name] = btn
                self.layout.add_widget(btn)

    def on_add_button_pressed(self, instance):
        self.sm.current = "contact_add_screen"
