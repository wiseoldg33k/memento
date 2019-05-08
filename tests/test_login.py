def test_it_creates_a_database_if_it_does_not_exist(state, backend):
    state.set_backend(backend=backend)
    assert state.db_should_be_created()


def test_it_does_not_create_a_database_if_it_exists(state, backend):
    state.set_backend(backend=backend)
    backend.init()
    assert not state.db_should_be_created()
