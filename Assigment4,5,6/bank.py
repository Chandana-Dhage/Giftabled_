class Bank:
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self.__balance:
            print("Withdrawal refused: insufficient balance")
            return False
        self.__balance -= amount
        return True

    def get_balance(self):
        return self.__balance


if __name__ == "__main__":
    account = Bank(1000)
    account.deposit(500)
    account.withdraw(200)
    print("Balance:", account.get_balance())
    account.withdraw(5000)
    print("Balance:", account.get_balance())