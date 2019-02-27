import bcrypt

class State:

    GENSALT_ROUNDS = 14

    def db_should_be_created(self):
        return not self.db_exists

    def hash_pin(self, pin):
        return bcrypt.hashpw(
                     pin.encode('utf-8'), 
                     bcrypt.gensalt(rounds=self.GENSALT_ROUNDS))