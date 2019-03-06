import bcrypt
import json
import base64
import hashlib

from cryptography.fernet import Fernet


class State:
    def __init__(self, salt):
        self.salt = salt

        self._data = {}

    def db_should_be_created(self):
        return not self.db_exists

    def hash_pin(self, pin):
        """
        This function transforms a PIN code into 
        a Fernet-compatible key in 2 steps:
        - convert the PIN code into fixed-size base64 hash to prevent 
          bcrypt failure if the key is >72 characters
        - convert the hash into a 32-bytes base64 hash to feed Fernet, 
          because that's its key format
        """
        fixed_size_password = base64.b64encode(
            hashlib.sha256(pin.encode("utf-8")).digest()
        )
        hashed = bcrypt.hashpw(fixed_size_password, self.salt)
        truncated = hashed[:32]
        return base64.b64encode(truncated)


    def dump(self, decryption_key, db_location):
        f = Fernet(decryption_key)
        encrypted_content = f.encrypt(json.dumps(self._data).encode('utf-8'))

        with open(db_location, 'wb') as db:
            db.write(encrypted_content)

        return True

    def load(self, decryption_key, db_location):
        with open(db_location, 'rb') as db:
            encrypted_content = db.read()

        f = Fernet(decryption_key)
        content = f.decrypt(encrypted_content)
        self._data = json.loads(content)

        return True
