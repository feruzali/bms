class Customer():
    def set_name(self, name):
        self.name = name

    def set_customer_id(self,id):
        self.customer_id = id

    def set_password(self,pwd):
        self.password = pwd

    def set_login_attempts(self,att):
        self.login_attempts = att
        if att == 0:
            self.status = "locked"

    def set_status(self,status):
        self.status = status

    def get_name(self):
        return self.name

    def get_customer_id(self):
        return self.customer_id

    def get_password(self):
        return self.password

    def get_login_attempts(self):
        return self.login_attempts

    def get_status(self):
        return self.status


class Account():

    def set_account_no(self,acc_no):
        self.account_no = acc_no

    def set_account_type(self,type):
        self.type = type

    def set_balance(self,bal):
        self.balance = bal

    def set_withdrawals_left(self,wd):
        self.withdrawals_left = wd

    def get_account_no(self):
        return self.account_no

    def get_balance(self):
        return self.balance

    def get_account_type(self):
        return self.type

    def get_withdrawals_left(self):
        return self.withdrawals_left



class Savings(Account):

    interest = 7.5
    min_balance = 0

    def open_account(self,amount):
        if amount < 0:
            print("Please input a valid amount")
            return False
        else:
            self.balance = amount
            return True

    def deposit(self,amount):
        if amount < 0:
            print("Please input a valid amount")
            return False
        else:
            self.balance += amount
            return True


    def withdraw(self,amount):
        if amount > self.balance:
            print("Sorry You don't have enough balance")
            return False
        else:
            self.balance -= amount
            return True

class Current(Account):

    interest = 0
    min_balance = 5000

    def open_account(self,amount):
        if amount < self.min_balance:
            print("Please input a valid amount")
            return False
        else:
            self.balance = amount
            return True

    def deposit(self,amount):
        if amount < 0:
            print("Please input a valid amount")
            return False
        else:
            self.balance += amount
            return True


    def withdraw(self,amount):
        if amount > self.balance:
            print("Sorry You don't have enough balance")
            return False
        elif self.balance - amount < 5000:
            print("Sorry You can't withdraw this much money as you need at least Rs",self.min_balance," to maintain this account")
            return False
        else:
            self.balance -= amount
            return True


class Fixed_Deposit(Account):

    min_balance = 1000

    def open_account(self,amount):
        if amount < self.min_balance:
            print("Please input a valid amount")
            return False
        else:
            self.balance = amount
            return True

    def set_deposit_term(self,term):
        self.deposit_term = term

    def get_deposit_term(self):
        return self.deposit_term
