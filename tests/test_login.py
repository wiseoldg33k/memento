import pytest
import time
from memento import State

@pytest.fixture
def slow_state():
    state = State()
    return state

@pytest.fixture
def state(slow_state):
    slow_state.GENSALT_ROUNDS = 1
    return slow_state


def test_it_creates_a_database_if_it_does_not_exist(state):
    state.db_exists = False
    assert state.db_should_be_created()


def test_it_does_not_create_a_database_if_it_exists(state):
    state.db_exists = True
    assert not state.db_should_be_created()

@pytest.mark.slow
@pytest.mark.parametrize('pincode', ['12345', '00000', 'éric'])
def test_pin_code_hashing_takes_more_than_a_second(slow_state, pincode):

    start = time.perf_counter()

    slow_state.hash_pin(pincode)

    end = time.perf_counter()

    elapsed = end - start

    assert elapsed > 1