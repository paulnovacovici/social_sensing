import pyrebase
import StockInfo
import StockTwitsClient as stc
import time as t

from datetime import datetime
from queue import PriorityQueue
from Scraper import Scraper
from StockSim import  StockSim

MONTHS = [None, 'January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

"""
Get sentiment as a percentage of a stock
@:param q is the Priority Queue of the stock to find
sentiment of
"""
def QueueSentiment(q):
    if (q.empty()):
        return 0

    queue_arr = list(q.queue)
    count = 0
    for data in queue_arr:
        sentiment = data[1]
        if sentiment:
            count += 1
    return 100*count/len(queue_arr)

"""
Buy stock with 80% of buying power
@:param top_stock
"""
def purchase_shares(top_stock):
    global sim, current_stock
    price = sim.get_stock_price(top_stock[0])
    bpwr = sim.get_buying_pwr()
    shares = int(bpwr * .8 / price)

    sim.buy_stock(top_stock[0], shares)
    current_stock = (top_stock[0], top_stock[1])

if __name__ == "__main__":
    config = {
        "apiKey" : "AIzaSyAKYTPbWbA0zvNNnO55CMBrInsL8NTXN1s",
        "authDomain" : "social-sensing-6d403.firebaseapp.com",
        "databaseURL" : "https://social-sensing-6d403.firebaseio.com/",
        "storageBucket" : "social-sensing-6d403.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)

    # Get a reference to the database service
    db = firebase.database()

    trending = [str(ticker) for ticker in stc.get_trending_stocks()]

    for stock in trending:
        if stock not in StockInfo.stock_info:
            StockInfo.stock_info[stock] = PriorityQueue(maxsize=50)

    # Start scraping data
    scraper = Scraper(trending)

    current_stock = ('', 0)

    sim = StockSim()
    count = 0
    while True:
        top_stock = ('', 0)
        for stock in trending:
            positive_sentiment = QueueSentiment(StockInfo.stock_info[stock])

            if positive_sentiment > top_stock[1]:
                top_stock = (stock, positive_sentiment)

        # if queues aren't populated there won't be a top_stock
        if top_stock[0] == '':
            continue

        # Check if current stock should be sold
        if current_stock[0] != '':
            if top_stock[0] != current_stock[0] and top_stock[1] >= QueueSentiment(
                    StockInfo.stock_info[current_stock[0]]):

                sim.sell_stock(current_stock[0], sim.get_shares(current_stock[0]))
                # sometimes Finance API doesn't have price of stock available
                try:
                    purchase_shares(top_stock)
                except KeyError:
                    current_stock = ('',0)
        else:
            # sometimes Finance API doesn't have price of stock available
            try:
                purchase_shares(top_stock)
            except KeyError:
                current_stock = ('', 0)

        acc_bal = sim.get_acc_bal()

        # every minute update database with account balance
        if count % 60 == 0:
            now = datetime.now()
            # push to DB
            db.child('%s %s, %s' % (MONTHS[now.month], now.day, now.year)).child('%s:%s' % (now.hour,now.minute)).set(acc_bal)
            count = 0

        t.sleep(5)
        count += 5