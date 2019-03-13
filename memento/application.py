import kivy
kivy.require('1.10.1')

# TODO: find a more elegant solution later
from kivy.config import Config
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 100)
Config.set('graphics', 'top',  100)

import bcrypt
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from memento.state import State
from memento.widgets.login import LoginWidget
from memento.widgets.createdb import CreateDBWidget

SALT_FILENAME = 'salt'
DB_FILENAME = 'memento.db'


class MementoApp(App):

    def build(self):
        if not os.path.isfile(SALT_FILENAME):
            with open(SALT_FILENAME, 'wb') as fsalt:
                fsalt.write(bcrypt.gensalt(14))

        with open(SALT_FILENAME, 'rb') as fsalt:
            salt = fsalt.read()

        state = State(salt=salt)
        sm = ScreenManager()

        create_screen = Screen(name='create_db_screen')
        create_screen.add_widget(CreateDBWidget(state=state, 
                                                db_filename=DB_FILENAME))
        sm.add_widget(create_screen)

        login_screen = Screen(name='login_screen')
        login_screen.add_widget(LoginWidget(state=state, 
                                            db_filename=DB_FILENAME))
        sm.add_widget(login_screen)

        if os.path.isfile(DB_FILENAME):
            sm.current = 'login_screen'
        else:
            sm.current = 'create_db_screen'

        return sm


if __name__ == '__main__':
    MementoApp().run()

