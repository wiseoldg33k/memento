import os
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


kivy.require("1.10.1")

# TODO: find a more elegant solution later

from kivy.config import Config  # noqa: E402

Config.set("graphics", "position", "custom")
Config.set("graphics", "left", 100)
Config.set("graphics", "top", 100)

Config.set("graphics", "width", "400")
Config.set("graphics", "height", "711")

from memento import DB_FILENAME, PROFILE_PICTURES_LOCATION  # noqa: E402
from memento.state import State  # noqa: E402
from memento.widgets.login import LoginWidget  # noqa: E402
from memento.widgets.createdb import CreateDBWidget  # noqa: E402
from memento.widgets.roster import RosterWidget  # noqa: E402
from memento.widgets.contact.add import ContactAddWidget  # noqa: E402
from memento.widgets.contact.edit import ContactEditWidget  # noqa: E402


class MementoApp(App):
    def build(self):

        if not os.path.isdir(PROFILE_PICTURES_LOCATION):
            os.makedirs(PROFILE_PICTURES_LOCATION)

        state = State()
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

        contact_edit_screen = Screen(name="contact_edit_screen")
        contact_edit_screen.add_widget(
            ContactEditWidget(state=state, sm=sm, screen=contact_edit_screen)
        )
        sm.add_widget(contact_edit_screen)

        if os.path.isfile(DB_FILENAME):
            sm.current = "login_screen"
        else:
            sm.current = "create_db_screen"

        # XXX: this is only for debug
        state.load(state.hash_pin("1234"), DB_FILENAME)
        state.set_edited_contact("Alice")
        sm.current = "contact_edit_screen"

        return sm


def main():
    MementoApp().run()


if __name__ == "__main__":
    main()
