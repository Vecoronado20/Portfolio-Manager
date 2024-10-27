import time
from time import strftime, localtime


class Dividend_Receipt:
    def __init__(self, amount):
        self.month = time.strftime("%m", localtime())
        self.day = time.strftime("%d", localtime())
        self.year = time.strftime("%Y", localtime())
        self.payment_amount = amount
        self.drip_shares = 0

    def __str__(self):
        if self.drip_shares == 0:
            return f'{self.month}/{self.day}/{self.year} : ${self.payment_amount:.2f}       DRIP Shares: Unavailable'
        else:
            return f'{self.month}/{self.day}/{self.year} : ${self.payment_amount:.2f}       DRIP Shares: {self.drip_shares:.4f}'

    def setDripShares(self, total_drip_shares):
        self.drip_shares = total_drip_shares
