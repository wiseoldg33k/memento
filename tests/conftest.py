import pytest
import os
import tempfile
from memento.state import State


@pytest.fixture
def pincode():
    return "12345"


@pytest.fixture
def state():
    state = State()
    return state


@pytest.fixture
def db_location():
    fd, name = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.remove(name)
    return name
