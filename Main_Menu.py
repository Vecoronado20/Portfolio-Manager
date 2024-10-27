import pickle
from os import system
from Portfolio import Portfolio
from Holding import Holding
import customtkinter as ctk
import tkinter as tk
from prettytable import PrettyTable, PLAIN_COLUMNS


def saveData():
    with open('portfolioData.txt', 'wb') as file:
        pickle.dump(portfolios, file)


table = PrettyTable()


def calcUsedColumnsHoldings(active_portfolio):
    holdingNum = 0
    for _ in active_portfolio.getHoldings():
        holdingNum += 1
    numUsedColumns = (holdingNum // 10) + 1
    if numUsedColumns == 0:
        numUsedColumns = 1
    totalColumns = numUsedColumns + 2
    return numUsedColumns, totalColumns


class Main_Menu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Portfolio Manager Home")
        ctk.set_appearance_mode("dark")
        self.mainMenu()

    def mainMenu(self):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text="Welcome to the Portfolio Manager.", font=("Georgia", 30))
        label.pack(padx=10, pady=20)
        button = ctk.CTkButton(self, text="Start New Portfolio", command=lambda: self.newPortfolio())
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="Delete Existing Portfolio", command=lambda: self.deletePortfolio())
        button1.pack(padx=10, pady=20)
        button2 = ctk.CTkButton(self, text="View Existing Portfolios", command=lambda: self.choosePortfolio())
        button2.pack(padx=10, pady=20)

    def newPortfolio(self):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text="Enter a name for the new portfolio", font=("Georgia", 20))
        label.pack(padx=10, pady=20)
        entry = ctk.CTkEntry(self, placeholder_text="New Portfolio Name")
        entry.pack(padx=10, pady=20)
        button = ctk.CTkButton(self, text="Create Portfolio", command=lambda: self.newPortfolioHandler(entry.get()))
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="Back to Main Menu", command=lambda: self.mainMenu())
        button1.pack(padx=10, pady=20)

    def newPortfolioHandler(self, name):
        match = False
        for portfolio in portfolios:
            if portfolio.getName() == name:
                match = True
                break
        if not match:
            portfolios.append(Portfolio(name))
            saveData()
            self.mainMenu()
            return
        self.newPortfolio()
        return

    def deletePortfolio(self):
        for widget in self.winfo_children():
            widget.destroy()
        portfolioToDelete = -1
        label = ctk.CTkLabel(self, text="Which portfolio would you like to delete?", font=("Georgia", 20))
        label.pack(padx=10, pady=20)
        buttons = []
        for portfolio in portfolios:
            buttons.append(ctk.CTkButton(self, text=f"{portfolio}", command=lambda target=portfolio: self.deleteHandler(target)))
        for button in buttons:
            button.pack(padx=10, pady=20)
        back = ctk.CTkButton(self, text="Back to Main Menu", command=lambda: self.mainMenu())
        back.pack(padx=10, pady=20)

    def deleteHandler(self, target):
        label = ctk.CTkLabel(self, text=f"Are you sure you would like to delete {target.getName()}?", font=("Georgia", 15))
        label.pack(padx=10, pady=30)
        button = ctk.CTkButton(self, text="Yes", command=lambda: self.deletePortfolioFinalization(target))
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="No", command=lambda: self.mainMenu())
        button1.pack(padx=10, pady=20)
        return

    def deletePortfolioFinalization(self, portfolio):
        portfolios.remove(portfolio)
        saveData()
        self.mainMenu()
        return

    def choosePortfolio(self):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text="Which portfolio would you like to view?", font=("Georgia", 20))
        label.pack(padx=10, pady=20)
        buttons = []
        for portfolio in portfolios:
            buttons.append(ctk.CTkButton(self, text=f"{portfolio}", command=lambda active_portfolio=portfolio: self.portfolioHome(active_portfolio)))
        for button in buttons:
            button.pack(padx=10, pady=20)
        back = ctk.CTkButton(self, text="Back to Main Menu", command=lambda: self.mainMenu())
        back.pack(padx=10, pady=20)

    def portfolioHome(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text=f"Welcome to the overview for {active_portfolio.getName()}!", font=("Georgia", 20))
        label.pack(padx=10, pady=10)
        label1 = ctk.CTkLabel(self, text=f"What would you like to do?", font=("Georgia", 15))
        label1.pack(padx=10, pady=10)
        button = ctk.CTkButton(self, text="Add a New Position", command=lambda: self.addHolding(active_portfolio))
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="Delete an Existing Position", command=lambda: self.deleteHolding(active_portfolio))
        button1.pack(padx=10, pady=20)
        button2 = ctk.CTkButton(self, text="Document a Dividend Payment", command=lambda: self.addDivPayment(active_portfolio))
        button2.pack(padx=10, pady=20)
        button3 = ctk.CTkButton(self, text="Document an Interest Payment", command=lambda: self.addInterestPayment(active_portfolio))
        button3.pack(padx=10, pady=20)
        button4 = ctk.CTkButton(self, text="Document a Non-Documented Dividend", command=lambda: self.addNonDocDiv(active_portfolio))
        button4.pack(padx=10, pady=20)
        button5 = ctk.CTkButton(self, text="Update Portfolio Yields, Equity, and P/L")
        button5.pack(padx=10, pady=20)
        button6 = ctk.CTkButton(self, text="Update Brokerage Cash", command=lambda: self.updateBrokerageCash(active_portfolio))
        button6.pack(padx=10, pady=20)
        button7 = ctk.CTkButton(self, text="Update Interest Rate", command=lambda: self.updateInterestRate(active_portfolio))
        button7.pack(padx=10, pady=20)
        button8 = ctk.CTkButton(self, text="Change a Daily Investment", command=lambda: self.changeDaily(active_portfolio))
        button8.pack(padx=10, pady=20)
        button9 = ctk.CTkButton(self, text="View Portfolio Data", command=lambda: self.viewPortfolio(active_portfolio))
        button9.pack(padx=10, pady=20)
        button10 = ctk.CTkButton(self, text="View Portfolio Overview Data")
        button10.pack(padx=10, pady=20)
        button11 = ctk.CTkButton(self, text="View Holding Info")
        button11.pack(padx=10, pady=20)
        button12 = ctk.CTkButton(self, text="Return to Main Menu", command=lambda: self.mainMenu())
        button12.pack(padx=10, pady=20)

    def addHolding(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=5)
        label = ctk.CTkLabel(self, text="New Holding Info", font=("Georgia", 30))
        label.grid(padx=10, pady=30, row=0, columnspan=4)
        label1 = ctk.CTkLabel(self, text="Enter Ticker Symbol: ", font=("Georgia", 15))
        ticker = ctk.CTkEntry(self)
        label1.grid(row=1, column=1)
        ticker.grid(row=1, column=2)
        label2 = ctk.CTkLabel(self, text="Enter Sector: ", font=("Georgia", 15))
        sector = ctk.CTkEntry(self)
        label2.grid(row=2, column=1)
        sector.grid(row=2, column=2)
        label3 = ctk.CTkLabel(self, text="Enter Investment Type (Stock/ETF): ", font=("Georgia", 15))
        type = ctk.CTkEntry(self)
        label3.grid(row=3, column=1)
        type.grid(row=3, column=2)
        label4 = ctk.CTkLabel(self, text="Enter Dividend Yield (%): ", font=("Georgia", 15))
        div_yield = ctk.CTkEntry(self)
        label4.grid(row=4, column=1)
        div_yield.grid(row=4, column=2)
        label5 = ctk.CTkLabel(self, text="Enter Expense Ratio (%): ", font=("Georgia", 15))
        exp_ratio = ctk.CTkEntry(self)
        label5.grid(row=5, column=1)
        exp_ratio.grid(row=5, column=2)
        label6 = ctk.CTkLabel(self, text="Enter Current Equity: ", font=("Georgia", 15))
        equity = ctk.CTkEntry(self)
        label6.grid(row=6, column=1)
        equity.grid(row=6, column=2)
        button = ctk.CTkButton(self, text="Add New Holding", command=lambda: self.addHoldingHandler(active_portfolio, ticker.get(), sector.get(), type.get(), div_yield.get(), exp_ratio.get(), equity.get()))
        button.grid(padx=10, pady=20, row=7, columnspan=4)
        button1 = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button1.grid(padx=10, pady=20, row=8, columnspan=4)

    def addHoldingHandler(self, active_portfolio, ticker, sector, type, div_yield, exp_ratio, equity):
        div_yield_final = float(div_yield) / 100
        exp_ratio_final = float(exp_ratio) / 100
        equity_final = float(equity)
        newHolding = Holding(ticker, sector, type, div_yield_final, exp_ratio_final, equity_final)
        newHolding.calculateData()
        active_portfolio.addHolding(newHolding)
        active_portfolio.updateData()
        saveData()
        self.portfolioHome(active_portfolio)

    def deleteHolding(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        numUsedColumns, totalColumns = calcUsedColumnsHoldings(active_portfolio)
        self.grid_columnconfigure(0, weight=5)
        for col in range(1, numUsedColumns):
            self.grid_columnconfigure(col, weight=1)
        self.grid_columnconfigure(numUsedColumns + 1, weight=5)
        label = ctk.CTkLabel(self, text="Which holding would you like to delete?", font=("Georgia", 20))
        label.grid(padx=10, pady=30, row=0, columnspan=totalColumns)
        buttons = []
        row_start = 1
        for holding in active_portfolio.getHoldings():
            buttons.append(ctk.CTkButton(self, text=f"{holding.getTicker()}", command=lambda target=holding: self.deleteHoldingHandler(active_portfolio, target, row_start, totalColumns)))
        for x, button in enumerate(buttons):
            row_start += 1
            if x > 10:
                row_start = 11
            button.grid(padx=10, pady=20, row=int(x % 9) + 1, column=int(x // 9) + 1)
        button = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button.grid(padx=10, pady=20, row=row_start + 1, columnspan=totalColumns)

    def deleteHoldingHandler(self, active_portfolio, target, row_start, columnTotal):
        label = ctk.CTkLabel(self, text=f"Are you sure you would like to delete {target.getTicker()}", font=("Georgia", 15))
        label.grid(padx=10, pady=30, row=row_start, columnspan=columnTotal)
        button = ctk.CTkButton(self, text="Yes", command=lambda: self.deleteHoldingFinalization(active_portfolio, target))
        button.grid(padx=10, pady=20, row=row_start + 1, columnspan=columnTotal)
        button1 = ctk.CTkButton(self, text="No", command=lambda: self.portfolioHome(active_portfolio))
        button1.grid(padx=10, pady=20, row=row_start + 2, columnspan=columnTotal)
        return

    def deleteHoldingFinalization(self, active_portfolio, target):
        active_portfolio.addNonDocDivPayment(target.getDivReinvested())
        active_portfolio.getHoldings().remove(target)
        active_portfolio.updateData()
        saveData()
        self.portfolioHome(active_portfolio)
        return

    def addDivPayment(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        numUsedColumns, totalColumns = calcUsedColumnsHoldings(active_portfolio)
        self.grid_columnconfigure(0, weight=5)
        for col in range(1, numUsedColumns):
            self.grid_columnconfigure(col, weight=1)
        self.grid_columnconfigure(numUsedColumns + 1, weight=5)
        label = ctk.CTkLabel(self, text="Which holding would you like to document a dividend payment for?", font=("Georgia", 20))
        label.grid(padx=10, pady=30, row=0, columnspan=numUsedColumns + 2)
        buttons = []
        row_start = 1
        for holding in active_portfolio.getHoldings():
            buttons.append(ctk.CTkButton(self, text=f"{holding.getTicker()}", command=lambda target=holding: self.addDivPaymentHandler(active_portfolio, target)))
        for x, button in enumerate(buttons):
            row_start += 1
            if x > 10:
                row_start = 11
            button.grid(padx=10, pady=20, row=int(x % 9) + 1, column=int(x // 9) + 1)
        button = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button.grid(padx=10, pady=20, row=row_start + 1, columnspan=totalColumns)

    def addDivPaymentHandler(self, active_portfolio, target):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text=f"What is the dividend payment from {target.getTicker()}?", font=("Georgia", 20))
        label.pack(padx=10, pady=20)
        entry = ctk.CTkEntry(self)
        entry.pack(padx=10, pady=20)
        button = ctk.CTkButton(self, text="Confirm Dividend Payment", command=lambda: self.addDivPaymentFinalization(active_portfolio, target, entry.get()))
        button.pack(padx=10, pady=20)

    def addDivPaymentFinalization(self, active_portfolio, target, amount):
        divPayment = float(amount)
        target.addDividend(divPayment)
        target.calculateData()
        active_portfolio.updateData()
        saveData()
        self.portfolioHome(active_portfolio)

    def addInterestPayment(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text=f"What was the interest payment for {active_portfolio.getName()}?", font=("Georgia", 25))
        label.pack(padx=10, pady=20)
        entry = ctk.CTkEntry(self)
        entry.pack(padx=10, pady=20)
        button = ctk.CTkButton(self, text="Confirm Interest Payment", command=lambda: self.addInterestPaymentHandler(active_portfolio, entry.get()))
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button1.pack(padx=10, pady=20)

    def addInterestPaymentHandler(self, active_portfolio, amount):
        interestPayment = float(amount)
        active_portfolio.addInterestPayment(interestPayment)
        active_portfolio.updateData()
        saveData()
        self.portfolioHome(active_portfolio)

    def addNonDocDiv(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text=f"What is the new non-documented dividend payment?", font=("Georgia", 25))
        label.pack(padx=10, pady=20)
        entry = ctk.CTkEntry(self)
        entry.pack(padx=10, pady=20)
        button = ctk.CTkButton(self, text="Confirm Dividend Payment", command=lambda: self.addNonDocDivHandler(active_portfolio, entry.get()))
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button1.pack(padx=10, pady=20)

    def addNonDocDivHandler(self, active_portfolio, amount):
        div_payment = float(amount)
        active_portfolio.addNonDocDivPayment(div_payment)
        active_portfolio.updateData()
        saveData()
        self.portfolioHome(active_portfolio)

    def updateBrokerageCash(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text=f"Current brokerage cash is ${active_portfolio.getBrokerageCash():,.2f}.", font=("Georgia", 25))
        label.pack(padx=10, pady=20)
        label1 = ctk.CTkLabel(self, text=f"What is the new brokerage cash total?", font=("Georgia", 25))
        label1.pack(padx=10, pady=20)
        entry = ctk.CTkEntry(self)
        entry.pack(padx=10, pady=20)
        button = ctk.CTkButton(self, text="Confirm Cash Total", command=lambda: self.updateBrokerageCashHandler(active_portfolio, entry.get()))
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button1.pack(padx=10, pady=20)

    def updateBrokerageCashHandler(self, active_portfolio, new_total):
        cash_total = float(new_total)
        active_portfolio.setBrokerageCash(cash_total)
        active_portfolio.updateData()
        saveData()
        self.portfolioHome(active_portfolio)

    def updateInterestRate(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text=f"Current interest rate is {active_portfolio.getInterestRate() * 100:.2f}%.", font=("Georgia", 25))
        label.pack(padx=10, pady=20)
        label1 = ctk.CTkLabel(self, text=f"What is the new interest rate on brokerage cash?", font=("Georgia", 25))
        label1.pack(padx=10, pady=20)
        entry = ctk.CTkEntry(self)
        entry.pack(padx=10, pady=20)
        button = ctk.CTkButton(self, text="Confirm Interest Rate", command=lambda: self.updateInterestRateHandler(active_portfolio, entry.get()))
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button1.pack(padx=10, pady=20)

    def updateInterestRateHandler(self, active_portfolio, new_rate):
        interest_rate = float(new_rate) / 100
        active_portfolio.setInterestRate(interest_rate)
        active_portfolio.updateData()
        saveData()
        self.portfolioHome(active_portfolio)

    def changeDaily(self, active_portfolio):
        for widget in self.winfo_children():
            widget.destroy()
        numUsedColumns, totalColumns = calcUsedColumnsHoldings(active_portfolio)
        self.grid_columnconfigure(0, weight=5)
        for col in range(1, numUsedColumns):
            self.grid_columnconfigure(col, weight=1)
        self.grid_columnconfigure(numUsedColumns + 1, weight=5)
        label = ctk.CTkLabel(self, text="Which holding would you like to change your daily investment for?", font=("Georgia", 20))
        label.grid(padx=10, pady=30, row=0, columnspan=numUsedColumns + 2)
        buttons = []
        row_start = 1
        for holding in active_portfolio.getHoldings():
            buttons.append(ctk.CTkButton(self, text=f"{holding.getTicker()}", command=lambda target=holding: self.changeDailyHandler(active_portfolio, target)))
        for x, button in enumerate(buttons):
            row_start += 1
            if x > 10:
                row_start = 11
            button.grid(padx=10, pady=20, row=int(x % 9) + 1, column=int(x // 9) + 1)
        button = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button.grid(padx=10, pady=20, row=row_start + 1, columnspan=totalColumns)

    def changeDailyHandler(self, active_portfolio, target):
        for widget in self.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self, text=f"The current daily investment for {target.getTicker()} is ${target.getDailyInvestment():.2f}", font=("Georgia", 25))
        label.pack(padx=10, pady=20)
        label1 = ctk.CTkLabel(self, text=f"What would you like to change it to?", font=("Georgia", 25))
        label1.pack(padx=10, pady=20)
        entry = ctk.CTkEntry(self)
        entry.pack(padx=10, pady=20)
        button = ctk.CTkButton(self, text="Confirm New Daily Investment", command=lambda: self.changeDailyFinalization(active_portfolio, target, entry.get()))
        button.pack(padx=10, pady=20)
        button1 = ctk.CTkButton(self, text="Return to Home", command=lambda: self.portfolioHome(active_portfolio))
        button1.pack(padx=10, pady=20)

    def changeDailyFinalization(self, active_portfolio, target, amount):
        new_daily = float(amount)
        target.setDaily(new_daily)
        active_portfolio.updateData()
        saveData()
        self.portfolioHome(active_portfolio)


try:
    with open('portfolioData.txt', 'rb') as file:
        portfolios = pickle.load(file)
except:
    portfolios = []

root = Main_Menu()
root.mainloop()
