import pytest
import time
import os
import tempfile

@pytest.fixture
def slow_state(state):
    state.salt = b'$2b$14$BMOTE4FHkpRb1tU1heKnFe'
    return state


def test_it_creates_a_database_if_it_does_not_exist(state):
    state.db_exists = False
    assert state.db_should_be_created()


def test_it_does_not_create_a_database_if_it_exists(state):
    state.db_exists = True
    assert not state.db_should_be_created()


@pytest.mark.slow
@pytest.mark.parametrize("pincode", ["12345", "00000", "éric"])
def test_pin_code_hashing_takes_more_than_a_second(slow_state, pincode):

    start = time.perf_counter()

    hashed = slow_state.hash_pin(pincode)

    end = time.perf_counter()

    elapsed = end - start

    assert elapsed > 1


def test_it_can_decrypt_encrypted_database(state, db_location, pincode):

    state._data = {'hello': 'world'}

    decryption_key = state.hash_pin(pincode)

    assert not os.path.isfile(db_location)

    state.dump(decryption_key, db_location)

    assert os.path.isfile(db_location)

    assert state.load(decryption_key, db_location)

    assert state._data['hello'] == 'world'