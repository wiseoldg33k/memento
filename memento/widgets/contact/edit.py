from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout


class TopSegment(StackLayout):
    def __init__(self, state, sm, screen, **kwargs):
        self.state = state
        self.sm = sm
        self.screen = screen
        super().__init__(**kwargs)

        self.screen.bind(on_pre_enter=self.update_widgets)

    def update_widgets(self, *args, **kwargs):
        contact = self.state.edited_contact

        if contact.profile_picture:
            pic = Image(source=contact.profile_picture)
        else:
            pic = Button(text="Set Picture")

        pic.size_hint = (0.2, 1)
        self.add_widget(pic)
        self.add_widget(
            Label(text="{}".format(contact.name), size_hint=(0.8, 1))
        )


class BottomSegment(StackLayout):
    def __init__(self, state, sm, screen, **kwargs):
        self.state = state
        self.sm = sm
        self.screen = screen
        super().__init__(**kwargs)
        self.add_widget(Label(text="Bottom Segment"))


class MiddleSegment(StackLayout):
    def __init__(self, state, sm, screen, **kwargs):
        self.state = state
        self.sm = sm
        self.screen = screen
        super().__init__(**kwargs)
        self.add_widget(Label(text="Middle Segment"))

        with self.canvas.before:
            Color(
                0, 0.6, 0.2, 0.4
            )  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ContactEditWidget(StackLayout):
    def __init__(self, state, sm, screen, **kwargs):
        self.state = state
        self.sm = sm
        self.screen = screen
        super().__init__(**kwargs)

        self.add_widget(
            TopSegment(state=state, sm=sm, screen=screen, size_hint=(1, 0.2))
        )
        self.add_widget(
            MiddleSegment(
                state=state, sm=sm, screen=screen, size_hint=(1, 0.6)
            )
        )
        self.add_widget(
            BottomSegment(
                state=state, sm=sm, screen=screen, size_hint=(1, 0.2)
            )
        )
