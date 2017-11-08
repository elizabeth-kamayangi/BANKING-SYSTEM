import random
class Bank:
    banks = {}
    """
    Bank model class 
    """

    def __init__(self, name, location, id=""):
        self.name = name
        self.location = location
        self.id = random.randint(1,10)
        self.__accounts = {}
        self.__customers = {}
        self.__tellers = {}
        self.__loans = {}

    def add_customer(self, customer, teller):
        if self.is_valid_teller(teller):
            customer_id = self.get_unique_id("customer")
            self.__customers.update({customer_id: customer})
            return customer_id
        else:
            raise Exception("Unauthorized access")

    def add_account(self, account, teller):
        if self.is_valid_teller(teller):
            self.__accounts.update({account.id: account})
        else:
            raise Exception("Unauthorized access")

    def add_teller(self, teller):
        teller.id = self.get_unique_id("teller")
        teller.bank = self
        self.__tellers.update({teller.id: teller})

    def add_loan(self, loan, teller):
        if self.is_valid_teller(teller):
            self.__loans.update({loan.id: loan})
        else:
            raise Exception("Unauthorized access")

    def is_valid_teller(self, teller):
        if teller.id in self.__tellers:
            return True
        return False

    def get_max_id(self, data):
        return max([int(y[len(self.name.lower().replace(" ", '') + "teller"):]) for y in list(data.keys())])

    def get_unique_id(self, qualifier):
        x = 0
        if qualifier.lower() in ["teller", "customer", "loan", "account"]:
            if qualifier.lower() == "teller":
                if not list(self.__tellers.keys()):
                    return self.name.lower().replace(" ", '') + qualifier.lower() + "1"
                x = self.get_max_id(self.__tellers)

            elif qualifier.lower() == "customer":
                if not list(self.__customers.keys()):
                    return self.name.lower().replace(" ", '') + qualifier.lower() + "1"
                x = x = self.get_max_id(self.__customers)

            elif qualifier.lower() == "loan":
                if not list(self.__loans.keys()):
                    return self.name.lower().replace(" ", '') + qualifier.lower() + "1"
                x = x = self.get_max_id(self.__loans)

            elif qualifier.lower() == "account":
                if not list(self.__accounts.keys()):
                    return self.name.lower().replace(" ", '') + qualifier.lower() + "1"
                x = x = self.get_max_id(self.__accounts)

            return self.name.lower().replace(" ", '') + qualifier.lower() + str(x)
        else:
            raise Exception("Invalid Qualifier")

    def get_customer(self, id):
        if id in self.__customers:
            return self.__customers[id]

    def get_account(self, id):
        if self.is_valid_account(id):
            return self.__accounts[id]

    def get_loan(self, id):
        if id in self.__loans:
            return self.__loans[id]

    def update_account(self, account_id, amount):
        if self.is_valid_account(account_id):
            new_amount = self.__accounts[account_id].get_account_balance() + amount
            self.__accounts[account_id].set_account_balance(new_amount)

    def is_valid_account(self, account_id):
        if not account_id:
            raise Exception("Invalid Account")
        if not account_id in self.__accounts:
            raise Exception("Invalid Account")
        return True

    def delete_account(self, account_id):
        if self.is_valid_account(account_id):
            del self.__accounts[account_id]

class Teller():
    def __init__(self, name, bank=None):
        self.id = None
        self.name = name
        self.bank = bank
        if self.bank:
            self.bank.add_teller(self)

    def collect_money(self, account_id, amount, qualifier):
        if qualifier == "deposit":
            self.bank.update_account(account_id, amount)

    def open_account(self, customer, account_type, amount):
        if account_type in ["savings", "checking"]:
            customer_id = None
            if not customer.get_account_id():
                customer_id = self.bank.add_customer(customer, self)

            elif not self.bank.get_customer(customer.get_account_id()):
                raise Exception("Customer already with another bank")

            account_id = self.bank.get_unique_id("account")
            if account_type == "savings":
                account = SavingsAccount(account_id, customer.get_account_id(), amount)
                self.bank.add_account(account, self)

            else:
                account = CheckingAccount(account_id, customer.get_account_id(), amount)
                self.bank.add_account(account, self)

            return {"account_id": account_id, "customer_id": customer_id}


        else:
            raise Exception("Invalid Account type")

    def close_account(self, account_id):
        self.bank.delete_account(account_id)

    def loan_request(self, customer, loan_type, amount):
        pass

    def provide_info(self, customer):
        pass

    def issue_card(self):
        pass

class Customer():
    def __init__(self, name, address, phone_no):
        self.__id = None
        self.name = name
        self.address = address
        self.phone_no = phone_no
        self.__account_id = None

    def general_inquiry(self, teller):
        pass

    def deposit_money(self, teller, account_id, amount):
        teller.collect_money(account_id, amount, "deposit")

    def withdraw_money(self, teller, account_id, amount):
        pass

    def open_account(self, teller, account_type, initial_amount):
        data = teller.open_account(self, account_type, initial_amount)
        self.__account_id = data["account_id"]
        if data["customer_id"]:
            self.__id = data["customer_id"]

    def close_account(self, teller, account_id):
        teller.close_account(self.account_id)
        self.__account_id = None

    def apply_for_loan(self, teller, loan_type, amount):
        pass

    def request_card(self):
        pass

    def get_account_id(self):
        return self.__account_id

    def get_customer_id(self):
        return self.__id

class Account():
    def __init__(self, id, customer_id, amount):
        self.id = id
        self.customer_id = customer_id
        self.__account_balance = amount

    def set_account_balance(self, amount):
        self.__account_balance = amount

    def get_account_balance(self):
        return self.__account_balance

class CheckingAccount(Account):
    def __init__(self, id, customer_id, amount):
        super().__init__(id, customer_id, amount)

class SavingsAccount(Account):
    def __init__(self, id, customer_id, amount):
        super().__init__(id, customer_id, amount)

class Loan():
    def __init__(self, id, loan_type, customer_id, amount):
        self.id = id
        self.loan_type = loan_type
        self.amount = amount
        self.customer_id = customer_id

