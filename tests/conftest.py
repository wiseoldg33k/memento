import pytest
import tempfile
import shutil
from memento.state import State
from memento.backend import Backend
from memento import hash_pincode


@pytest.fixture
def pincode():
    return "12345"


@pytest.fixture
def db_location():
    name = tempfile.mkdtemp(suffix=".db")
    yield name
    shutil.rmtree(name)


@pytest.fixture
def backend(db_location, pincode):
    return Backend(db_location, hash_pincode(pincode))


@pytest.fixture
def state(backend):
    state = State()
    state.set_backend(backend=backend)
    return state
