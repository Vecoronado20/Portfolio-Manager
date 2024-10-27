import time
from time import strftime, localtime
import yfinance as yf
from Dividend_Receipt import Dividend_Receipt
from Stock_Data_Handler import Stock_Data_Handler

# Holds all relevant information for one stock/etf including aggregated totals and dividend receipts
class Holding:
    def __init__(self, ticker, sector, type, div_yield, exp_ratio, equity):
        self.ticker = ticker
        self.sector = sector
        self.type = type
        self.diversity = 0
        self.div_yield = div_yield
        self.exp_ratio = exp_ratio
        self.weighted_exp_ratio = 0
        self.equity = equity
        self.est_annual_div = 0
        self.daily_investment = 0
        self.daily_div_increase = 0
        self.p_l = 0
        self.div_reinvested = 0
        self.cost_basis = 0
        self.adj_cost_basis = 0
        self.adj_div_yield = div_yield
        self.div_history = []
        self.current_price = 0
        self.drip_shares = 0

    def calculateData(self):
        self.setAnnualDiv()
        self.setCostBasis()
        self.setAdjCostBasis()

    def setDiversity(self, new_diversity):
        self.diversity = new_diversity

    def setDivYield(self, new_div_yield):
        self.div_yield = new_div_yield

    def setWeightedExpRatio(self):
        self.weighted_exp_ratio = self.diversity * self.exp_ratio

    def setEquity(self, new_equity):
        self.equity = new_equity

    def setAnnualDiv(self):
        self.est_annual_div = self.div_yield * self.equity

    def setDaily(self, new_daily):
        self.daily_investment = new_daily

    def setDailyDivIncrease(self):
        self.daily_div_increase = self.div_yield * self.daily_investment

    def setP_L(self, new_p_l):
        self.p_l = new_p_l

    def setCostBasis(self):
        self.cost_basis = self.equity - self.p_l

    def setAdjCostBasis(self):
        self.adj_cost_basis = self.cost_basis - self.div_reinvested

    def setAdjDivYield(self):
        if self.adj_cost_basis >= .01:
            self.adj_div_yield = self.est_annual_div / self.adj_cost_basis
        else:
            self.adj_div_yield = 0.0

    def setCurrentPrice(self, price):
        self.current_price = price

    def setDripShares(self, amount):
        self.drip_shares = amount

    # Adds dividend to the total for this particular stock and creates a receipt for future tracking purposes
    def addDividend(self, div_amount, stock_data_handler):
        if div_amount > 0:
            self.div_reinvested += div_amount
            new_receipt = Dividend_Receipt(div_amount)
            self.div_history.append(new_receipt)
            # Calculate Approximate DRIP Shares
            self.calculateDripShares(div_amount, new_receipt, stock_data_handler)

    def calculateDripShares(self, div_amount, receipt, stock_data_handler):
        self.drip_shares = 0
       # dripShares = div_amount / stock_data_handler.getDayAvg(self.getTicker())
       # self.drip_shares += dripShares
        receipt.setDripShares(0)

    def getTicker(self):
        return self.ticker

    def getDiversity(self):
        return self.diversity

    def getDivYield(self):
        return self.div_yield

    def getExpRatio(self):
        return self.exp_ratio

    def getWeightedExpRatio(self):
        return self.weighted_exp_ratio

    def getEquity(self):
        return self.equity

    def getAnnualDiv(self):
        return self.est_annual_div

    def getDailyInvestment(self):
        return self.daily_investment

    def getDailyDivIncrease(self):
        return self.daily_div_increase

    def getP_L(self):
        return self.p_l

    def getDivReinvested(self):
        return self.div_reinvested

    def getCostBasis(self):
        return self.cost_basis

    def getAdjCostBasis(self):
        return self.adj_cost_basis

    def getCurrentPrice(self):
        return self.current_price

    # Produces stock info list for portfolio holdings view
    def getDataList(self):
        return [self.ticker, self.sector, self.type, f"{self.diversity * 100:.2f}%", f"{self.div_yield * 100:.2f}%", f"{self.exp_ratio * 100:.2f}%", f"{self.weighted_exp_ratio * 100:.4f}%", f"${self.equity:,.2f}", f"${self.est_annual_div:,.2f}", f"${self.daily_investment:,.2f}", f"${self.daily_div_increase:,.4f}", f"${self.p_l:,.2f}", f"${self.div_reinvested:,.2f}", f"${self.cost_basis:,.2f}", f"${self.adj_cost_basis:,.2f}", f"{self.adj_div_yield * 100:.2f}%", f"{self.drip_shares:.4f}"]

    def getDivHistory(self):
        return self.div_history
