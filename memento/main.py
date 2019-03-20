import kivy


import bcrypt
import os

from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from memento.state import State
from memento.widgets.login import LoginWidget
from memento.widgets.createdb import CreateDBWidget
from memento.widgets.roster import RosterWidget
from memento.widgets.contact import ContactAddWidget

kivy.require("1.10.1")

# TODO: find a more elegant solution later


Config.set("graphics", "position", "custom")
Config.set("graphics", "left", 100)
Config.set("graphics", "top", 100)

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '711')

SALT_FILENAME = "salt"
DB_FILENAME = "memento.db"


class MementoApp(App):
    def build(self):
        if not os.path.isfile(SALT_FILENAME):
            with open(SALT_FILENAME, "wb") as fsalt:
                fsalt.write(bcrypt.gensalt(14))

        with open(SALT_FILENAME, "rb") as fsalt:
            salt = fsalt.read()

        state = State(salt=salt)
        sm = ScreenManager()

        create_screen = Screen(name="create_db_screen")
        create_screen.add_widget(
            CreateDBWidget(state=state, db_filename=DB_FILENAME)
        )
        sm.add_widget(create_screen)

        login_screen = Screen(name="login_screen")
        login_screen.add_widget(
            LoginWidget(state=state, sm=sm, db_filename=DB_FILENAME)
        )
        sm.add_widget(login_screen)

        roster_screen = Screen(name="roster_screen")
        roster_widget = RosterWidget(state=state, sm=sm)
        roster_screen.add_widget(roster_widget)
        roster_screen.bind(on_pre_enter=roster_widget.on_pre_enter)
        sm.add_widget(roster_screen)

        contact_add_screen = Screen(name="contact_add_screen")
        contact_add_screen.add_widget(ContactAddWidget(state=state, sm=sm))
        sm.add_widget(contact_add_screen)

        if os.path.isfile(DB_FILENAME):
            sm.current = "login_screen"
        else:
            sm.current = "create_db_screen"

        return sm


if __name__ == "__main__":
    MementoApp().run()
