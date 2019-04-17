import pytest
from memento.backend import Backend
from memento.models import Contact
from memento import hash_pincode


def test_it_can_create_a_backend(db_location, pincode):
    assert Backend(db_location, hash_pincode(pincode))


@pytest.fixture
def backend(db_location, pincode):
    return Backend(db_location, hash_pincode(pincode))


def test_backend_can_save_object(backend):
    c = Contact(name="John")

    backend.save(c)
    assert c.id is not None


def test_get_object_by_id():
    pass


def test_get_object_by_attribute():
    pass


def test_get_all_objects():
    pass
