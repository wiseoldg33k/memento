import pytest
from memento.contact import Contact
from memento.state import to_json
import json


def test_it_can_serialize_contact_instance():
    contact = Contact(name="John Doe")
    assert json.dumps(contact, default=to_json)


def test_it_can_save_an_already_loaded_database_without_passing_location_again(
    state, db_location, pincode
):
    key = state.hash_pin(pincode)
    state.dump(key, db_location)
    state.load(key, db_location)

    assert state.dump()


def test_it_cannot_save_a_database_that_has_not_been_loaded(state):
    with pytest.raises(RuntimeError):
        state.dump()


def test_it_can_load_contacts_from_state(state):
    state.add_contact(name="John")
    state.add_contact(name="Jane")

    expected = sorted(["John", "Jane"])
    output = [c.name for c in state.list_contacts()]

    assert sorted(output) == expected
