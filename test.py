import yfinance as yf

holding = yf.Ticker('SCHD')
print(holding.get_info())