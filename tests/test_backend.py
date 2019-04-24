import pytest
from memento.backend import Backend, ResultSet
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


def test_get_object_by_id(backend):
    c = Contact(name="John")
    backend.save(c)

    found = backend.find(Contact, id=c.id)

    assert found.one().id == c.id


def test_get_object_by_attribute(backend):
    c = Contact(name="John")
    backend.save(c)

    found = backend.find(Contact, name=c.name)

    assert found.one().name == c.name


def test_get_all_objects(backend):
    names = ("Alice", "Bob", "Charles")

    for name in names:
        c = Contact(name=name)
        backend.save(c)

    objects = backend.all(Contact)

    assert sorted([o.name for o in objects]) == sorted(names)


def test_resultset_returns_one_items_when_calling_one_method():
    x = object()
    res = ResultSet([x])

    assert res.one() is x


def test_resultset_raises_when_calling_one_with_more_than_one_item():
    x = object()
    res = ResultSet([x, x])

    with pytest.raises(RuntimeError):
        res.one()
