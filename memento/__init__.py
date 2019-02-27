import bcrypt
import base64
import hashlib


class State:
    def __init__(self, salt):
        self.salt = salt

    def db_should_be_created(self):
        return not self.db_exists

    def hash_pin(self, pin):
        fixed_size_password = base64.b64encode(
            hashlib.sha256(pin.encode("utf-8")).digest()
        )
        return bcrypt.hashpw(fixed_size_password, self.salt)

    def dump(self, decryption_key, db_location):
        pass