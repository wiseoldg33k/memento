import base64
import hashlib

DB_FILENAME = "memento.db"
PROFILE_PICTURES_LOCATION = "pp"


def hash_pincode(pin):
    fixed_size_password = base64.b64encode(
        hashlib.sha256(pin.encode("utf-8")).digest()
    )
    truncated = fixed_size_password[:32]
    return base64.b64encode(truncated)
