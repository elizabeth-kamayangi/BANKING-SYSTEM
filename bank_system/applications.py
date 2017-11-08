import random
class Application:
    banks = {}

    def register_bank(self, bank):

        if bank in self.banks.keys():
            return False
        else:
            self.banks[bank] = bank
        return True

    def account(self):
        return '000333' + str(random.randint(99,200))

