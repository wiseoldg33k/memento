from . import hash_pincode
from .models import Contact


def to_json(obj):
    return obj.__dict__


class State:
    def __init__(self):
        self.backend = None

        # transient state
        self._edited_contact = None

    def set_backend(self, backend):
        self.backend = backend

    @property
    def edited_contact(self):
        return self._edited_contact

    def set_edited_contact(self, name):
        for contact in self.list_contacts():
            if contact.name == name:
                self._edited_contact = contact
                return True

        raise ValueError("contact {} not found".format(name))

    def db_should_be_created(self):
        return not self.backend.initialized

    def hash_pin(self, pin):
        return hash_pincode(pin)

    def add_contact(self, name, profile_picture=""):
        contact = Contact(name=name, profile_picture=profile_picture)
        self.backend.save(contact)

    def list_contacts(self):
        return self.backend.all(Contact)
