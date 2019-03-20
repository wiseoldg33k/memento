import os


def test_it_creates_a_database_if_it_does_not_exist(state):
    state.db_exists = False
    assert state.db_should_be_created()


def test_it_does_not_create_a_database_if_it_exists(state):
    state.db_exists = True
    assert not state.db_should_be_created()


def test_it_can_decrypt_encrypted_database(state, db_location, pincode):

    state._data["hello"] = "world"

    decryption_key = state.hash_pin(pincode)

    assert not os.path.isfile(db_location)

    state.dump(decryption_key, db_location)

    assert os.path.isfile(db_location)

    assert state.load(decryption_key, db_location)

    assert state._data["hello"] == "world"
