import os
import uuid
import logging

from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

INIT_MARKER = ".init"


class ResultSet(list):
    def one(self):
        if len(self) > 1:
            raise RuntimeError("too many items for one()")
        return self[0]


class Backend:
    def __init__(self, db_location, key):
        self.db_location = db_location
        self.key = key
        self._f = Fernet(self.key)

        self.marker_filename = os.path.join(self.db_location, INIT_MARKER)

    @property
    def initialized(self):
        return os.path.isfile(self.marker_filename)

    def init(self):
        with open(self.marker_filename, "w"):
            logger.info("backend initialized")

    def save(self, obj):
        if not hasattr(obj, "id") or obj.id is None:
            obj.id = uuid.uuid4()

        obj_type = obj.__class__.__name__.lower()

        type_folder = os.path.join(self.db_location, obj_type)

        if not os.path.isdir(type_folder):
            os.makedirs(type_folder)

        object_filename = os.path.join(type_folder, str(obj.id))

        schema = obj.Meta()

        with open(object_filename, "wb") as db:
            content = schema.dumps(obj).encode("utf-8")
            encrypted_content = self._f.encrypt(content)
            db.write(encrypted_content)

    def find(self, klass, **kwargs):
        obj_type = klass.__name__.lower()
        type_folder = os.path.join(self.db_location, obj_type)

        schema = klass.Meta()

        result = ResultSet()

        for filename in os.listdir(type_folder):
            object_filename = os.path.join(type_folder, filename)

            with open(object_filename, "rb") as db:
                encrypted_content = db.read()
                content = self._f.decrypt(encrypted_content)
                obj = schema.loads(content.decode("utf-8"))

                keep = True
                if kwargs:
                    for attr, value in kwargs.items():
                        if not getattr(obj, attr) == value:
                            keep = False

                if keep:
                    result.append(obj)

        return result

    def all(self, klass):
        return self.find(klass=klass)
