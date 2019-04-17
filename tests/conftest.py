import pytest
import tempfile
import shutil
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
    name = tempfile.mkdtemp(suffix=".db")
    print(name)
    yield name
    shutil.rmtree(name)
