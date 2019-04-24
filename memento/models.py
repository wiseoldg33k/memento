from marshmallow import Schema, fields, post_load


class Contact:
    class Meta(Schema):
        id = fields.UUID(required=True)
        name = fields.Str(required=True)
        profile_picture = fields.Str(required=False)

        @post_load
        def make_contact(self, data):
            ident = data.pop("id")
            c = Contact(**data)
            c.id = ident
            return c

    def __init__(self, name, profile_picture=""):
        self.name = name
        self.profile_picture = profile_picture
