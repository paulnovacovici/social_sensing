import unittest

import FinanceAPI
from StockSim import StockSim

class UnitTests(unittest.TestCase):
    def test_portfolio(self):
        stock_sim = StockSim()
        stock_sim.buy_stock("MSFT",20)
        stock_sim.buy_stock("AAPL",40)

        portfolio = stock_sim.portfolio
        num_shares = 0

        self.assertEqual(len(portfolio),2)
        for ticker,shares in portfolio.items():
            num_shares += shares

        self.assertEqual(num_shares,60)

    def test_api(self):
        stock_sim = StockSim()
        try:
            stock_sim.get_stock_price("GOOG")
        except:
            # Test if api get's information
            self.fail()
        else:
            self.assertTrue(True)

    # May not work if new 52 week low gets hit after code has been written
    def test_52Low(self):
        lo52 = FinanceAPI.get52WeekLow("GOOG")
        self.assertEqual(lo52, "727.54")

    # May not work if new 52 week high gets hit after code has been written
    def test_52Hi(self):
        hi52 = FinanceAPI.get52WeekHi("GOOG")
        self.assertEqual(hi52, "1,048.39")

if __name__ == "__main__":
    unittest.main()