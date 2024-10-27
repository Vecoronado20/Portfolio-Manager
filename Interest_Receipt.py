import time
from time import strftime, localtime


class Interest_Receipt:
    def __init__(self, amount):
        self.month = time.strftime("%m", localtime())
        self.day = time.strftime("%d", localtime())
        self.year = time.strftime("%Y", localtime())
        self.payment_amount = amount

    def __str__(self):
        return f'{self.month}/{self.day}/{self.year} : ${self.payment_amount:.2f}'