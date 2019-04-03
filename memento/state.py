import json
import base64
import hashlib

from cryptography.fernet import Fernet

from .contact import Contact


def to_json(obj):
    return obj.__dict__


class State:
    def __init__(self):
        self._data = {"contacts": []}

        self.__key = None
        self.__db_location = None

    def db_should_be_created(self):
        return not self.db_exists

    def hash_pin(self, pin):
        fixed_size_password = base64.b64encode(
            hashlib.sha256(pin.encode("utf-8")).digest()
        )
        truncated = fixed_size_password[:32]
        return base64.b64encode(truncated)

    def dump(self, decryption_key=None, db_location=None):
        if decryption_key is None:
            decryption_key = self.__key

        if db_location is None:
            db_location = self.__db_location

        if decryption_key is None or db_location is None:
            raise RuntimeError(
                "for a clean state, decryption_key and "
                "db_location must be passed explicitly"
            )

        f = Fernet(decryption_key)
        content = json.dumps(self._data, default=to_json).encode("utf-8")
        encrypted_content = f.encrypt(content)

        with open(db_location, "wb") as db:
            db.write(encrypted_content)

        return True

    def load(self, decryption_key, db_location):
        with open(db_location, "rb") as db:
            encrypted_content = db.read()

        f = Fernet(decryption_key)
        content = f.decrypt(encrypted_content)
        self._data = json.loads(content)

        self._data["contacts"] = [
            Contact(**data) for data in self._data["contacts"]
        ]

        self.__key = decryption_key
        self.__db_location = db_location

        return True

    def add_contact(self, name, profile_picture):
        self._data["contacts"].append(
            Contact(name=name, profile_picture=profile_picture)
        )

    def list_contacts(self):
        return self._data["contacts"]
