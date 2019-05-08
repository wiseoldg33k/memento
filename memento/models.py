from marshmallow import Schema, fields, post_load


class Event(Schema):
    date = fields.DateTime(required=True)
    description = fields.String(required=True)


class Contact:
    class Meta(Schema):
        id = fields.UUID(required=True)
        name = fields.Str(required=True)
        profile_picture = fields.Str(required=False)
        events = fields.List(fields.Nested(Event))

        @post_load
        def make_contact(self, data):
            ident = data.pop("id")
            c = Contact(**data)
            c.id = ident
            return c

    def __init__(self, name, profile_picture="", events=None):
        self.name = name
        self.profile_picture = profile_picture
        if events is None:
            events = []
        self.events = events
