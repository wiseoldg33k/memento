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
    state.add_contact(name="John", profile_picture=None)
    state.add_contact(name="Jane", profile_picture=None)

    expected = sorted(["John", "Jane"])
    output = [c.name for c in state.list_contacts()]

    assert sorted(output) == expected


def test_it_can_set_currently_edited_contact(state):
    state.add_contact(name="John", profile_picture=None)
    assert state.edited_contact is None
    state.set_edited_contact("John")
    assert state.edited_contact.name == "John"


def test_it_raises_an_exception_when_aiming_at_missing_contact(state):
    state.add_contact(name="John", profile_picture=None)
    with pytest.raises(ValueError):
        state.set_edited_contact("Karl")
