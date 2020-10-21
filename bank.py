from abc import *
import random
"""
>>>B = Bank()
>>>M = Manager('John', B)
Hello, John You are a Manger
>>>C1 = Customer('Mary', B)
Hello, Mary You are a Customer
>>>print(C1)
John
>>>C1.openAccount(1000, 'Savings Account')
Welcome to your Account!
1000
>>>C1.deposit(1000)
1999
>>>C1.withdraw(100)
1897
>>>C2 = Customer('Josie', B)
Hello, Josie You are a Customer
>>>C2.openAccount(300, 'Checking Account')
Welcome to your Account!
300
>>>A = Assistant('Henry', B)
Hello, Henry You are an Assistant
>>>A.transfer(C1, 100, C2)
'Marys new balance is: $900... Josies new balance is: $400'
>>>M = Manager('Phil', B)
Hello, Phil You are a Manager
>>>M.deactivate(C1)
Here is your remaing money: $100
'Account deactivated'
>>>C1.deposit(1000)
'Your account is inactive'
>>>M.reactivate(C1, 100)
'A Savings Account has a minimum balance of $250'
>>>M.reactivate(C1, 250)
'Account reactivated'
>>>M.getID(C1)
0000
>>>T = Teller('Bob', B)
Hello, Bob You are a Teller
>>>T.getName(C1)
Mary
>>>ck = Check(C2, 1000)
>>>C2.deposit(ck)
1400
>>>C1.deposit(ck)
250
>>>M.loan(C1, 10000000)
'You need 1000 to earn a loan with a Savings Account'
>>>C1.deposit(1000)
1249
>>>M.loan(C1, 100000)
12490



"""

class Bank:
    def __init__(self):
        self.accounts = []


    def openAccount(self, amount, account_type, active):
        """Open an account_type for holder and deposit amount."""
        if account_type == 'Savings Account':
            account = SavingsAccount(self, amount, active)
            #account.deposit(amount)
        elif account_type == 'Checking Account':
            account = CheckingAccount(self, amount, active)
            #account.deposit(amount)
        else:
            return'somthing went wrong'


        self.accounts.append(account)

        return account


    def payInterest(self):
        """Pay interest to all accounts."""
        for account in self.accounts:
            account.deposit((account.balance * account.INTEREST)+ account.balance)



class Account(ABC):

    INTEREST = 0.01


    def __init__(self, account_holder, balance, active=True):
        self.account_holder= account_holder
        self.balance = balance
        self.__id=self.__createID
        self.active = True

    @property
    def __createID(self):
        return random.randint(100,9000)

    @property
    def getID(self):
        return self.__id

    def setID(self, new_id):
        self.__id=new_id



    def deposit(self, amount):
        if isinstance(amount, (int,float)):
            self.balance = self.balance + amount
            return self.balance

        elif isinstance(amount, Check):
            if (not amount.cashed) and amount.check_amount>0:
                self.balance+=amount.check_amount
                amount.cashed=True
                return self.balance
            else:
                return 'you are trying to steal money'

        else:
            return 'invalid operation'

    def withdraw(self, amount):
        if isinstance(amount, (int,float)):
            if amount > self.balance:
                return 'Not enough funds'
            self.balance = self.balance - amount
            return self.balance
        else:
            return 'invalid operation'

    def loan(self, amount):
        self.balance = self.balance + amount
        return self.balance





class CheckingAccount(Account):
    WITHDRAW_FEE = 1

    def __init__(self, account_holder, balance, active=True):
        self.account_holder= account_holder
        self.balance = balance
        self.__id=self.__createID
        self.active = True

    @property
    def __createID(self):
        return random.randint(100,9000)

    @property
    def getID(self):
        return self.__id

    def setID(self, new_id):
        self.__id=new_id



    def withdraw(self, amount):
        return Account.withdraw(self, amount + CheckingAccount.WITHDRAW_FEE)

    def withdraw_transfer(self, amount):
        return Account.withdraw(self, amount)

    def deosit(self, amount):
        return Account.deposit(self, amount)

    def deposit_transfer(self, amount):
        return Account.deposit(self, amount)

    def greeting(self):
        return f'Welcome to your Checking Account!'

    def loan(self, amount):
        if self.balance >= 100:
            return Account.loan(self, amount)

        else:
            return 'You need 100 dollars to get a Loan with a Checking Account'





class SavingsAccount(Account):
    DEPOSIT_FEE = 1
    WITHDRAW_FEE = 2
    MIN_BALANCE = 250


    def __init__(self, holder, balance, active= True):
        super().__init__(holder, balance, active)
        print(self.greeting())


    def greeting(self):
        return f'Welcome to your Account!'

    def deposit(self, amount):
        if isinstance(amount, Check):
            return Account.deposit(self, amount)
        else:
            return Account.deposit(self, amount-SavingsAccount.DEPOSIT_FEE)

    def deposit_transfer(self, amount):
        return Account.deposit(self, amount)


    def withdraw(self, amount):
        if self.balance-amount+ SavingsAccount.WITHDRAW_FEE>=SavingsAccount.MIN_BALANCE:
            return Account.withdraw(self, amount + SavingsAccount.WITHDRAW_FEE)
        return 'min balance error withdraw'

    def withdraw_transfer(self, amount):
        if self.balance-amount >= SavingsAccount.MIN_BALANCE:
            return Account.withdraw(self, amount)
        return 'min balance error withdraw_transfer'

    def loan(self, amount):
        if self.balance >= 1000:
            return Account.loan(self, amount)
        return 'You need 1000 dolars to get a Loan with a Savings Account'




class Person(ABC):
    def __init__(self, name):
        self.name = name


    @abstractmethod
    def title(self):
        raise NotImplementedError('Subclass calls this method')


    def createID(self):
        return random.randint(100,9000)


    def getID(self):
        return self.id

    def setID(self, new_id):
        self.id=new_id






class Manager(Person):



    def __init__(self, name, Bank):
        super().__init__(name)
        self.id = Person.createID(self)
        print(self.title())
        self.Bank = Bank





    def title(self):
        return f'Hello, {self.name} You are a Manager'


    def getID(self, Person):
        return Person.id


    def deactivate(self, Person):
        Person.myAccount.active = False
        print(f'Here is your remaining money: ${Person.myAccount.balance}')
        Person.myAccount.balance = 0
        return 'Account deactivated'

    def reactivate(self, Person, amount):
        if isinstance(Person.myAccount, SavingsAccount):
            if amount >= SavingsAccount.MIN_BALANCE:
                Person.myAccount.active = True
            else:
                return f'A Savings Account has a minimum balance of $250'
        else:
            Person.myAccount.active = True
        return 'Account reactivated'

    def getName(self, Person):
        return Person.name

    def payInterest(self):
        """Pay interest to all accounts."""
        for Account in self.Bank.accounts:
            Account.deposit(Account.balance * Account.INTEREST)
            return Account.balance

    def loan(self, Person, amount):
        if isistance(Person.myAccount.account_type, SavingsAccount):
            SavingsAccount.loan(self, amount)
        else:
            CheckingAccount.loan(self, amount)









class Customer(Person):

    def __init__(self, name, Bank):
        super().__init__(name)
        self.id = Person.createID(self)
        print(self.title())
        self.Bank = Bank
        self.myAccount = None


    def title(self):
        return f'Hello, {self.name} You are a Customer'



    def __str__(self):
        return f'{self.name}'

    def openAccount(self, amount, account_type, active = True):
        self.myAccount = self.Bank.openAccount(amount, account_type, active)
        return self.myAccount.balance

    def deposit(self, amount):
        if self.myAccount.active == True:
            self.myAccount.deposit(amount)
            return self.myAccount.balance
        else:
            return 'Your account is inactive'



    def withdraw(self, amount):
        if self.myAccount.active == True:
            self.myAccount.withdraw(amount)
            return self.myAccount.balance
        else:
            return 'Your account is inactive'



















class Assistant(Person):

    def __init__(self, name, Bank):
        super().__init__(name)
        self.id = Person.createID(self)
        print(self.title())
        self.Bank = Bank

    def title(self):
        return f'Hello, {self.name} You are an Assistant'

    def transfer(self, sender,  amount, reciever):
        if sender.myAccount.balance>amount and sender.myAccount.active == True and reciever.myAccount.active == True:
            sender.myAccount.withdraw_transfer(amount)
            reciever.myAccount.deposit_transfer(amount)
            return f'{sender}s new balance is: ${sender.myAccount.balance}.... ${reciever}s new balance is: {reciever.myAccount.balance}'
        else:
            return f'There is not enough money in {sender}s account'

    def approveLoan(self, amount):
        return Account.loan(self, amount)




class Teller(Person):

    def __init__(self, name, Bank):
        super().__init__(name)
        print(self.title())
        self.Bank = Bank

    def title(self):
        return f'Hello, {self.name} You are a Teller'

    def getName(self, Person):
        return Person.name

class Check:


    def __init__(self, pay_to, amount):
        self.pay_to=pay_to
        self.check_amount=amount
        self.cashed=False
        self.fee=0

    def __str__(self):
        return 'Pay to the order of: {} ${}'.format(self.pay_to, self.check_amount+self.fee)

    def __repr__(self):
        return f'Cashed: {self.cashed}'

    def __sub__(self, other):
        if isinstance(other, (int,float)):
            self.check_amount-=other
            self.fee=other
            return self