class State:

    def db_should_be_created(self):
        return not self.db_exists