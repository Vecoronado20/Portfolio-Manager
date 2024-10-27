import Holding
import yfinance as yf
from Interest_Receipt import Interest_Receipt


# Holds all relevant info for portfolios including holdings and interest receipts
class Portfolio:
    def __init__(self, name):
        self.name = name
        self.holdings = []
        self.total_diversity = 0
        self.total_weighted_exp_ratio = 0
        self.total_equity = 0
        self.total_annual_div = 0
        self.total_daily_investments = 0
        self.total_daily_div_increase = 0
        self.total_p_l = 0
        self.total_div_reinvested = 0
        self.total_cost_basis = 0
        self.total_adj_cost_basis = 0
        self.brokerage_cash = 0
        self.cash_interest = 0
        self.non_documented_div = 0
        self.interest_rate = 0
        self.interest_history = []
        self.graph_points = []

    def __str__(self):
        return f"{self.name} - Total Equity: ${self.total_equity:,.2f}"

    def calculateTotalEquity(self):
        equity = 0
        for holding in self.holdings:
            equity += holding.getEquity()
        self.total_equity = equity

    def calculateDiversity(self):
        self.calculateTotalEquity()
        for holding in self.holdings:
            holding.setDiversity(holding.getEquity() / self.total_equity)

    def calculateWeightedExpenseRatio(self):
        for holding in self.holdings:
            holding.setWeightedExpRatio()

    def calculateDailyDivIncrease(self):
        for holding in self.holdings:
            holding.setDailyDivIncrease()

    def calculateAdjDivYield(self):
        for holding in self.holdings:
            holding.setAdjDivYield()

    def updateHoldings(self):
        for holding in self.holdings:
            holding.calculateData()

    # Adds interest payment to total and creates a receipt object to track the payment in the future
    def addInterestPayment(self, interest_amount):
        self.cash_interest += interest_amount
        new_receipt = Interest_Receipt(interest_amount)
        self.interest_history.append(new_receipt)

    def addNonDocDivPayment(self, div_amount):
        self.non_documented_div += div_amount

    def setBrokerageCash(self, cash_amount):
        self.brokerage_cash = cash_amount

    def setInterestRate(self, new_interest_rate):
        self.interest_rate = new_interest_rate

    def getYield(self):
        return self.total_annual_div / self.total_equity

    def getCostBasisYield(self):
        return self.total_annual_div / self.total_cost_basis

    def getAdjDivYield(self):
        return self.total_annual_div / self.total_adj_cost_basis

    def getDailyYield(self):
        if self.total_daily_investments > 0:
            return self.total_daily_div_increase / self.total_daily_investments
        else:
            return 0

    def getAdjP_L(self):
        return self.total_equity - self.total_adj_cost_basis

    def getAnnualInterest(self):
        return self.brokerage_cash * self.interest_rate

    def getAnnualDivIncrease(self):
        return self.total_daily_div_increase * 252

    def getAnnualExpCost(self):
        return self.total_equity * self.total_weighted_exp_ratio

    # Determine cumulative column totals by summing each investment
    def calculateColumnTotals(self):
        self.total_diversity = 0
        self.total_weighted_exp_ratio = 0
        self.total_equity = 0
        self.total_annual_div = 0
        self.total_daily_investments = 0
        self.total_daily_div_increase = 0
        self.total_p_l = 0
        self.total_div_reinvested = 0
        self.total_cost_basis = 0
        self.total_adj_cost_basis = 0
        for holding in self.holdings:
            self.total_diversity += holding.getDiversity()
            self.total_weighted_exp_ratio += holding.getWeightedExpRatio()
            self.total_equity += holding.getEquity()
            self.total_annual_div += holding.getAnnualDiv()
            self.total_daily_investments += holding.getDailyInvestment()
            self.total_daily_div_increase += holding.getDailyDivIncrease()
            self.total_p_l += holding.getP_L()
            self.total_div_reinvested += holding.getDivReinvested()
            self.total_cost_basis += holding.getCostBasis()
            self.total_adj_cost_basis += holding.getAdjCostBasis()
        self.total_adj_cost_basis -= (self.non_documented_div + self.cash_interest)

    def updateData(self):
        self.updateHoldings()
        self.calculateDiversity()
        self.calculateWeightedExpenseRatio()
        self.calculateDailyDivIncrease()
        self.calculateColumnTotals()
        self.calculateAdjDivYield()

    def addHolding(self, newHolding):
        self.holdings.append(newHolding)
        self.updateData()

    def addGraphPoint(self, currValue):
        self.graph_points.append(currValue)

    def getName(self):
        return self.name

    def getHoldings(self):
        return self.holdings

    def getHolding(self, index):
        return self.holdings[index]

    def getTotalEquity(self):
        return self.total_equity

    def getBrokerageCash(self):
        return self.brokerage_cash

    def getInterestRate(self):
        return self.interest_rate

    def getInterestHistory(self):
        return self.interest_history
    
    def getGraphPoints(self):
        return self.graph_points

    # Creates a row of total values for the overall portfolio holdings view
    def getDataList(self):
        return ["Total", "-", "-", f"{self.total_diversity * 100:.2f}%", f"{self.getYield() * 100:.2f}%", "-", f"{self.total_weighted_exp_ratio * 100:.4f}%", f"${self.total_equity:,.2f}", f"${self.total_annual_div:,.2f}", f"${self.total_daily_investments:,.2f}", f"${self.total_daily_div_increase:,.4f}", f"${self.total_p_l:,.2f}", f"${self.total_div_reinvested:,.2f}", f"${self.total_cost_basis:,.2f}", f"${self.total_adj_cost_basis:,.2f}", f"{self.getAdjDivYield() * 100:.2f}%", "-"]

    # Creates a row of total values for the manual entry items view
    def getManualList(self):
        return [f"${self.brokerage_cash:,.2f}", f"${self.cash_interest:,.2f}", f"${self.non_documented_div:,.2f}", f"{self.interest_rate * 100:.2f}%"]

    # Creates a row of aggregated values for the portfolio summary view
    def getCalculatedList(self):
        return [f"{self.getYield() * 100:.2f}%", f"{self.getCostBasisYield() * 100:.2f}%", f"{self.getAdjDivYield() * 100:.2f}%", f"{self.getDailyYield() * 100:.2f}%", f"${self.getAdjP_L():,.2f}", f"${self.getAnnualInterest():,.2f}", f"${self.getAnnualDivIncrease():,.2f}", f"${self.getAnnualExpCost():,.2f}"]
