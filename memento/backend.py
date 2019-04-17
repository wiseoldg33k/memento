import uuid
import os
from cryptography.fernet import Fernet
from marshmallow import Schema


class Backend:
    def __init__(self, db_location, key):
        self.db_location = db_location
        self.key = key

    def save(self, obj):
        if not hasattr(obj, "id") or obj.id is None:
            obj.id = str(uuid.uuid4())

        obj_type = obj.__class__.__name__.lower()

        type_folder = os.path.join(self.db_location, obj_type)

        if not os.path.isdir(type_folder):
            os.makedirs(type_folder)

        object_filename = os.path.join(type_folder, obj.id)

        class ObjectSchema(Schema):
            class Meta:
                fields = tuple(obj.__dict__.keys())

        schema = ObjectSchema()

        with open(object_filename, "wb") as db:
            f = Fernet(self.key)
            content = schema.dumps(obj).data.encode("utf-8")
            encrypted_content = f.encrypt(content)
            db.write(encrypted_content)
