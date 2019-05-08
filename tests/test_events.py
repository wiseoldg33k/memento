from memento.models import Contact
from datetime import datetime


def test_it_can_add_events_to_a_contact(backend):
    c = Contact(name="John")
    c.events = [{"date": datetime.now(), "description": "had lunch with Jane"}]

    backend.save(c)

    found = backend.find(Contact, name=c.name)

    found_contact = found.one()
    assert found_contact.name == c.name
    assert found_contact.events[0]["description"] == "had lunch with Jane"
