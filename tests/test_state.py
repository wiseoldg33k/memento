import pytest


def test_it_can_load_contacts_from_state(state):
    state.add_contact(name="John")
    state.add_contact(name="Jane")

    expected = sorted(["John", "Jane"])
    output = [c.name for c in state.list_contacts()]

    assert sorted(output) == expected


def test_it_can_set_currently_edited_contact(state):
    state.add_contact(name="John")
    assert state.edited_contact is None
    state.set_edited_contact("John")
    assert state.edited_contact.name == "John"


def test_it_raises_an_exception_when_aiming_at_missing_contact(state):
    state.add_contact(name="John")
    with pytest.raises(ValueError):
        state.set_edited_contact("Karl")
