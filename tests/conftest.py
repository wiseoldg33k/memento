import pytest
import os
import tempfile
from memento import State


@pytest.fixture
def pincode():
    return "12345"


@pytest.fixture
def state():
    salt = b"$2b$04$d7JNTkkjB3vLqmMMoX/Mzu"
    state = State(salt=salt)
    return state


@pytest.fixture
def db_location():
    fd, name = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.remove(name)
    return name
