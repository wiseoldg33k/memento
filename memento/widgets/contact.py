import os
import shutil

from hashlib import md5

from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView

from memento import PROFILE_PICTURES_LOCATION


class LoadImageDialog(StackLayout):
    def __init__(self, sm, profile_picture, **kwargs):
        self.sm = sm
        self.profile_picture = profile_picture
        super().__init__(**kwargs)

        self.file_list = FileChooserIconView(
            size_hint=(1, 0.8),
            path=os.getcwd(),
            multiselect=False,
            filters=["*.jpg", "*.jpeg"],
        )
        self.add_widget(self.file_list)

        box = BoxLayout(size_hint=(1, 0.2))

        self.load_button = Button(text="Load")
        box.add_widget(self.load_button)
        self.load_button.bind(on_press=self.on_load_button_pressed)

        self.add_widget(box)

    def on_load_button_pressed(self, instance, *args, **kwargs):
        if self.file_list.selection:
            filename = self.file_list.selection.pop()
            with open(filename, "rb") as f:
                hashed_filename = md5(f.read()).hexdigest()
                pp_name = os.path.join(
                    PROFILE_PICTURES_LOCATION, "{}.jpg".format(hashed_filename)
                )
                shutil.copy(filename, pp_name)
                self.profile_picture["filename"] = pp_name
                self.dlg.dismiss()


class ContactAddWidget(StackLayout):
    def __init__(self, state, sm, **kwargs):
        self.state = state
        self.sm = sm
        self.profile_picture = {}
        super().__init__(**kwargs)

        self.name = TextInput(
            multiline=False,
            hint_text="Name",
            password=False,
            size_hint=(1, 0.2),
        )
        self.add_widget(self.name)

        self.add_button = Button(text="Add", size_hint=(1, 0.1))
        self.add_widget(self.add_button)
        self.add_button.bind(on_press=self.on_add_button_pressed)

        self.cancel_button = Button(text="Cancel", size_hint=(1, 0.1))
        self.add_widget(self.cancel_button)
        self.cancel_button.bind(on_press=self.on_cancel_button_pressed)

        self.add_image_button = Button(text="Add Picture", size_hint=(1, 0.1))
        self.add_widget(self.add_image_button)
        self.add_image_button.bind(on_press=self.on_add_image_button_pressed)

    def on_add_button_pressed(self, instance):
        self.state.add_contact(
            name=self.name.text,
            profile_picture=self.profile_picture.get("filename", ""),
        )
        self.state.dump()
        self.sm.current = "roster_screen"
        self.name.text = ""

    def on_cancel_button_pressed(self, instance):
        self.sm.current = "roster_screen"
        self.name.text = ""

    def on_add_image_button_pressed(self, instance):
        content = LoadImageDialog(
            sm=self.sm, profile_picture=self.profile_picture
        )
        popup = Popup(
            title="Load image", content=content, size_hint=(0.9, 0.9)
        )
        content.dlg = popup
        popup.open()
