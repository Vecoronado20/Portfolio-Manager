import pickle
import chardet
import charset_normalizer
import charset_normalizer.md__mypyc
from os import system
import yfinance as yf
import time
from time import strftime, localtime
from Portfolio import Portfolio
from Holding import Holding
from prettytable import PrettyTable
from Stock_Data_Handler import Stock_Data_Handler


def saveData():
    with open('portfolioData.txt', 'wb') as file:
        pickle.dump(portfolios, file)


def clear():
    system('cls')


def startup():
    while True:
        clear()
        saveData()
        print("Welcome to the Portfolio Data Collector.")
        print("(a) Start New Portfolio")
        print("(b) Delete Existing Portfolio")
        print("(c) View Existing Portfolios")
        print("(d) Save (Developer Option)")
        answer = input("Enter choice: ")
        if answer.lower() == "a":
            createPortfolio()
        elif answer.lower() == "b":
            deletePortfolio()
        elif answer.lower() == "c":
            choosePortfolio()
        elif answer.lower() == "d":
            saveData()


def showPortfolioList():
    print("Portfolio List:\n")
    for index, portfolio in enumerate(portfolios):
        print(f"({index}) {portfolio}")


def showHoldingList(portfolio):
    print("Portfolio:")
    for index, holding in enumerate(portfolio.getHoldings()):
        print(f"({index}) {holding.getTicker()}")


def createPortfolio():
    while True:
        clear()
        match = False
        answer = input("Enter a name for the new portfolio: ")
        for portfolio in portfolios:
            if portfolio.getName() == answer:
                match = True
                break
        if not match:
            portfolios.append(Portfolio(answer))
            saveData()
            break


def deletePortfolio():
    while True:
        clear()
        showPortfolioList()
        answer = input("\nWhich portfolio would you like to delete? (Type 'Back' to return to Home): ")
        if answer.lower() == "back":
            return
        if int(answer) < len(portfolios):
            target = portfolios[int(answer)]
            answer1 = input(f"\nAre you sure you want to delete {target.getName()}?: ")
            if answer1.lower() == "yes" or answer1.lower() == "y":
                portfolios.remove(target)
                saveData()
                break


def choosePortfolio():
    while True:
        clear()
        showPortfolioList()
        answer = input("\n Which portfolio would you like to view? (Type 'Back' to return to Home): ")
        if answer.lower() == "back":
            break
        if int(answer) < len(portfolios):
            portfolioHome(portfolios[int(answer)])
            break


def portfolioHome(portfolio):
    portfolio.updateData()
    while True:
        clear()
        print(f"Welcome to the overview for {portfolio.getName()}!")
        print("What would you like to do?")
        print("(a) Add a New Position")
        print("(b) Delete an Existing Position")
        print("(c) Document a Dividend Payment")
        print("(d) Document an Interest Payment")
        print("(e) Document a Non-Documented Dividend")
        print("(f) Update Portfolio Yields, Equity, and P/L")
        print("(g) Update Brokerage Cash")
        print("(h) Update Interest Rate")
        print("(i) Change a Daily Investment")
        print("(j) View Portfolio Data")
        print("(k) View Portfolio Overview Data")
        print("(l) View Holding Info")
        print("(m) Return to Home")
        answer = input("Enter choice: ")
        answer = answer.lower()
        if answer == "a":
            addHolding(portfolio)
        elif answer == "b":
            deleteHolding(portfolio)
        elif answer == "c":
            addDivPayment(portfolio)
        elif answer == "d":
            addInterestPayment(portfolio)
        elif answer == "e":
            addNonDocDiv(portfolio)
        elif answer == "f":
            updateData(portfolio)
        elif answer == "g":
            updateBrokerageCash(portfolio)
        elif answer == "h":
            updateInterestRate(portfolio)
        elif answer == "i":
            changeDaily(portfolio)
        elif answer == "j":
            viewPortfolio(portfolio)
        elif answer == "k":
            viewPortfolioOverview(portfolio)
        elif answer == "l":
            viewHoldingInfo(portfolio)
        elif answer == "m":
            break


def addHolding(portfolio):
    clear()
    ticker = input("Enter Ticker Symbol: ")
    sector = input("Enter Sector: ")
    type = input("Enter Investment Type (Stock/ETF): ")
    div_yield = float(input("Enter Dividend Yield (%): ")) / 100
    if type.lower() == "stock":
        exp_ratio = 0.0
    else:
        exp_ratio = float(input("Enter Expense Ratio (%): ")) / 100
    equity = float(input("Enter Current Equity: "))
    newHolding = Holding(ticker, sector, type, div_yield, exp_ratio, equity)
    newHolding.calculateData()
    portfolio.addHolding(newHolding)
    portfolio.updateData()
    saveData()


def deleteHolding(portfolio):
    clear()
    showHoldingList(portfolio)
    answer = int(input("Which holding would you like to delete?: "))
    if answer < len(portfolio.getHoldings()):
        holding = portfolio.getHolding(answer)
        answer1 = input(f"\nAre you sure you want to remove {holding.getTicker()} from your portfolio?: ")
        if answer1.lower() == "yes" or answer1.lower() == "y":
            portfolio.addNonDocDivPayment(holding.getDivReinvested())
            portfolio.getHoldings().remove(holding)
            portfolio.updateData()
            saveData()


def addDivPayment(portfolio):
    clear()
    showHoldingList(portfolio)
    answer = int(input("Which holding would you like to document a dividend payment for?: "))
    clear()
    if answer < len(portfolio.getHoldings()):
        holding = portfolio.getHolding(answer)
        div_payment = float(input(f"What is the payment from {holding.getTicker()}? ($): "))
        holding.addDividend(div_payment, stock_data_handler)
        holding.calculateData()
        portfolio.updateData()
        saveData()


def addInterestPayment(portfolio):
    clear()
    answer = float(input("What is the interest payment? ($): "))
    portfolio.addInterestPayment(answer)
    portfolio.updateData()
    saveData()


def addNonDocDiv(portfolio):
    clear()
    answer = float(input("What is the new non-documented dividend payment? ($): "))
    portfolio.addNonDocDivPayment(answer)
    portfolio.updateData()
    saveData()


def updateData(portfolio):
    clear()
    answer = input("Would you like to update a single holding or all holdings?: ")
    if answer.lower() == "single" or answer.lower() == "one":
        clear()
        showHoldingList(portfolio)
        answer1 = int(input("Which holding would you like to update?: "))
        if answer1 < len(portfolio.getHoldings()):
            clear()
            updateHolding(portfolio.getHolding(answer1))
    elif answer.lower() == "all":
        for holding in portfolio.getHoldings():
            clear()
            updateHolding(holding)
    portfolio.updateData()
    saveData()


def updateHolding(holding):
    print(f"Updating info for {holding.getTicker()}\n")
    #new_div_yield = stock_data_handler.getDivYield(holding.getTicker())
    #holding.setDivYield(float(new_div_yield))
    print(f"Current Dividend Yield is {holding.getDivYield() * 100:.2f}%")
    print("Type 'S' for same value.")
    new_div_yield = input(f"What is the current dividend yield for {holding.getTicker()}? (%): ")
    if new_div_yield != 'S' and new_div_yield != 's':
        holding.setDivYield(float(new_div_yield) / 100)
    print(f"Current Equity: ${holding.getEquity():.2f}")
    print("Type 'S' for same value.")
    new_equity = input(f"What is your current equity for {holding.getTicker()}? ($): ")
    if new_equity != 'S' and new_equity != 's':
        holding.setEquity(float(new_equity))
    print(f"Current P/L: ${holding.getP_L():.2f}")
    print("Type 'S' for same value.")
    new_p_l = input(f"What is your current P/L for {holding.getTicker()}? ($): ")
    if new_p_l != 'S' and new_p_l != 's':
        holding.setP_L(float(new_p_l))


def updateBrokerageCash(portfolio):
    clear()
    print(f"Current brokerage cash is ${portfolio.getBrokerageCash():,.2f}.")
    answer = float(input("What is the new amount of brokerage cash in the account? ($): "))
    portfolio.setBrokerageCash(answer)
    portfolio.updateData()
    saveData()


def updateInterestRate(portfolio):
    clear()
    print(f"Current interest rate is {portfolio.getInterestRate() * 100:.2f}%.")
    answer = float(input("What is the new interest rate on brokerage cash? (%): "))
    portfolio.setInterestRate(answer / 100)
    portfolio.updateData()
    saveData()


def changeDaily(portfolio):
    clear()
    showHoldingList(portfolio)
    answer = int(input("Which holding would you like to change your daily investment for?: "))
    clear()
    if answer < len(portfolio.getHoldings()):
        holding = portfolio.getHolding(answer)
        print(f"The current daily investment for {holding.getTicker()} is ${holding.getDailyInvestment():.2f}")
        new_daily = float(input("What would you like to change it to? ($): "))
        holding.setDaily(new_daily)
        portfolio.updateData()
        saveData()


def viewPortfolio(portfolio):
    clear()
    table.field_names = ("Ticker", "Sector", "Type", "Diversity", "Div Yield", "Exp Ratio", "Wgt Exp Ratio", "Equity", "Annual Div",
                         "Dly Investment", "Dly Div Inc", "P/L", "Divs Reinvested", "CB", "Adj CB", "ACB Yield", "DRIP Shares")
    for holding in portfolio.getHoldings():
        table.add_row(holding.getDataList())
    table.add_row(portfolio.getDataList())
    print(table)
    print("* DRIP Shares are an approximation of total shares bought by dividends as of 05/04/2023\n")
    input("Press 'Enter' to return to menu: ")
    table.clear()


def viewPortfolioOverview(portfolio):
    clear()
    print("Manually Entered Data:")
    table.field_names = ("Brokerage Cash", "Cash Interest", "Non-Documented Div", "Interest Rate")
    table.add_row(portfolio.getManualList())
    print(table)
    print("\nCalculated Data:")
    table1.field_names = ("Div Yield", "Yield on CB", "Yield on ACB", "Dly Inv Yield", "Adj P/L", "Est Ann Interest", "Est Ann Div Inc", "Est Ann Exp Cost")
    table1.add_row(portfolio.getCalculatedList())
    print(table1)
    print("\nInterest History:\n")
    for interest_payment in reversed(portfolio.getInterestHistory()):
        print(f" {interest_payment}")
    input("\nPress 'Enter' to return to menu: ")
    table.clear()
    table1.clear()


def viewHoldingInfo(portfolio):
    clear()
    showHoldingList(portfolio)
    answer = int(input("Which holding do you want to view?: "))
    clear()
    if answer < len(portfolio.getHoldings()):
        holding = portfolio.getHolding(answer)
        #print(f"Holding Overview For {holding.getTicker()}\n")
        #holding.setCurrentPrice(0)
        #holding.setCurrentPrice(stock_data_handler.getOpenPrice(holding.getTicker()))
        #print(f"Latest Open Price: ${holding.getCurrentPrice():.2f}\n")
        print("Stock Info/Data:")
        table.field_names = ("Ticker", "Sector", "Type", "Diversity", "Div Yield", "Exp Ratio", "Wgt Exp Ratio", "Equity", "Annual Div",
                             "Dly Investment", "Dly Div Inc", "P/L", "Divs Reinvested", "CB", "Adj CB", "ACB Yield", "DRIP Shares")
        table.add_row(holding.getDataList())
        print(table)
        print("* DRIP Shares are an approximation of total shares bought by dividends as of 05/04/2023")
        print("\nDividend History:\n")
        for payment in reversed(holding.getDivHistory()):
            print(f" {payment}")
        if len(holding.getDivHistory()) == 0:
            print(" No Dividend History")
        print("")
        input("Press 'Enter' to return to menu: ")
        table.clear()


try:
    with open('portfolioData.txt', 'rb') as file:
        portfolios = pickle.load(file)
except:
    portfolios = []


viewingPortfolio = None
table = PrettyTable()
table1 = PrettyTable()
stock_data_handler = Stock_Data_Handler()
startup()
