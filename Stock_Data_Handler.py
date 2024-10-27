import yfinance as yf


class Stock_Data_Handler:
    def __init__(self):
        self.saved_holdings = {}

    def retrieveStockInfo(self, ticker):
        if not self.checkIfPreloaded(ticker):
            stock = yf.Ticker(ticker)
            stock_info = stock.get_info()
            self.saved_holdings.update({ticker: stock_info})

    def checkIfPreloaded(self, ticker):
        if ticker in self.saved_holdings.keys():
            return True
        else:
            return False

    def getDivYield(self, ticker):
        self.retrieveStockInfo(ticker)
        try:
            current_div_yield = self.saved_holdings[ticker]['yield']
            return current_div_yield
        except KeyError:
            pass
        try:
            current_div_yield = self.saved_holdings[ticker]['dividendYield']
            return current_div_yield
        except KeyError:
            current_div_yield = 0
            return current_div_yield

    def getOpenPrice(self, ticker):
        self.retrieveStockInfo(ticker)
        return self.saved_holdings[ticker]['open']

    def getDayAvg(self, ticker):
        self.retrieveStockInfo(ticker)
        dayLow = self.saved_holdings[ticker]['dayLow']
        dayHigh = self.saved_holdings[ticker]['dayHigh']
        dayAvg = (dayLow + dayHigh) / 2
        return dayAvg