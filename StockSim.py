import MyLogger
import FinanceAPI

class StockSim(object):
    #Deposit default is $100,000
    #Portfolio starts out as empty
    def __init__(self, acc_bal=100000):
        self.bpwr = acc_bal
        self.portfolio = {}

    def get_buying_pwr(self):
        return self.bpwr

    """
    @:param ticker is ticker of stock to sell without '$'
    """
    def get_shares(self, ticker):
        return self.portfolio[ticker]

    """
    description: Get's the account balance by
    adding up the value of each share.
    """
    def get_acc_bal(self):
        count = self.bpwr
        for ticker, shares in self.portfolio.items():
            price = self.get_stock_price(ticker)
            count += price * shares
        return count

    """
    @:param ticker ticker of stock that user want's price from
    """
    def get_stock_price(self, ticker):
        return float(FinanceAPI.getStockPrice(ticker).replace(",",""))

    """
    @:param ticker of the stock without '$'
    @:shares number of shares of stock to buy
    """
    def buy_stock(self, ticker, shares):
        price = self.get_stock_price(ticker)

        if (price * shares <= self.bpwr):
            self.bpwr -= price * shares
        else:
            MyLogger.ewrite("Not enough funds to purchase %d shares of %s at price %d" % (shares,ticker,price))
            raise ValueError("Not enough funds")

        if ticker in self.portfolio:
            self.portfolio[ticker] += shares
        else:
            self.portfolio[ticker] = shares

        MyLogger.write("BUY\t%s\t%d" % (ticker,shares))

    """
    @:param ticker of stock wanting to be sold must be without '$'
    @:param shares number of shares to be sold
    """
    def sell_stock(self, ticker, shares):
        price = self.get_stock_price(ticker)

        if ticker not in self.portfolio:
            MyLogger.ewrite("Do not have %s" % ticker)
            raise ValueError("Do not have %s" % ticker)

        if (shares <= self.portfolio[ticker]):
            self.bpwr += price * shares
            self.portfolio[ticker] -= shares
        else:
            MyLogger.ewrite("Do not have %d shares of %s" % (shares,ticker))
            raise ValueError("Do not have %d shares" % shares)

        MyLogger.write("SELL\t%s\t%d" % (ticker, shares))

