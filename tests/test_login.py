def test_it_creates_a_database_if_it_does_not_exist(state):
    state.db_exists = False
    assert state.db_should_be_created()


def test_it_does_not_create_a_database_if_it_exists(state):
    state.db_exists = True
    assert not state.db_should_be_created()
