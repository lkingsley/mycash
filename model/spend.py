from model.transaction import Transaction

class Spend(Transaction):
    def __init__(self, amount, method, date):
        super().__init__(amount, method, date)
    def __str__(self):
        return f"Spend {{amount={self.amount}, method={self.method}, date={self.date}}}"