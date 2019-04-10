from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class TopSegment(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Top Segment"))


class BottomSegment(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Bottom Segment"))


class MiddleSegment(StackLayout):
    def __init__(self, **kwargs):
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
    def __init__(self, state, sm, **kwargs):
        self.state = state
        self.sm = sm
        super().__init__(**kwargs)

        self.add_widget(TopSegment(size_hint=(1, 0.2)))
        self.add_widget(MiddleSegment(size_hint=(1, 0.6)))
        self.add_widget(BottomSegment(size_hint=(1, 0.2)))
