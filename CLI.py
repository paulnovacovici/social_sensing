import FinanceAPI
from StockSim import StockSim

def print_options(portfolio,bpwr,acc_bal):
    print("Portfolio: " + portfolio)
    print("Buying Power: " + bpwr)
    print("Account Balance: " + acc_bal)
    print("B     Buy Stock")
    print("S     Sell Stock")
    print("P     Get Stock Price")
    print("Q     Quit")
    print("Command: ",end='')


if __name__ == "__main__":
    stock_sim = StockSim()

    while(True):
        print_options(str(stock_sim.portfolio),
                      str(stock_sim.get_buying_pwr()),
                      str(stock_sim.get_acc_bal()))
        cmd = input()

        if cmd == 'B':
            print("Enter stock ticker: ",end="")
            ticker = input()
            print("Enter amount of shares: ",end="")
            shares = int(input())
            try:
                stock_sim.buy_stock(ticker, shares)
            except ValueError as e:
                print(e)
        elif cmd == 'S':
            print("Enter stock ticker: ", end="")
            ticker = input()
            print("Enter amount of shares: ", end="")
            shares = int(input())
            try:
                stock_sim.sell_stock(ticker,shares)
            except ValueError as e:
                print(e)
        elif cmd == 'P':
            print("Enter stock ticker: ", end="")
            ticker = input()
            print(FinanceAPI.getStockPrice(ticker))
        elif cmd == "Q":
            break
        else:
            print("Enter a correct command")

        print("[PRESS ENTER]")
        input()

