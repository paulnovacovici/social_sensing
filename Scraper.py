from threading import Thread
from queue import PriorityQueue
from TwitterClient import TwitterClient

import MyLogger
import StockInfo
import time as t
import StockTwitsClient as stc

class Scraper(object):
    def __init__(self, trending):
        self.trending = trending
        self.tc = TwitterClient()
        self.start_twitter_stream()
        thread = Thread(target=self.start_stock_twits_stream)
        thread.start()

    """
    Soft copy of trending
    @:param trending
    """
    def set_trending(self,trending):
        for i in range(len(trending)):
            self.trending[i] = trending[i]

    def start_twitter_stream(self):
        self.tc.get_tweets_stream(self.trending)

    def close_twitter_stream(self):
        pass
        self.tc.close_stream()

    def start_stock_twits_stream(self):
        while (StockInfo.flag):
            messages = stc.get_stock_streams(self.trending)['messages']
            for message in messages:
                # Check what stock the message is talking about
                for stock in self.trending:
                    if stock not in message['body']:
                        continue

                    if stock not in StockInfo.stock_info:
                        StockInfo.stock_info[stock] = PriorityQueue(maxsize=50)

                    # Check if someone is spamming stream
                    if self.isDup(StockInfo.stock_info[stock],message['body']):
                        continue

                    if StockInfo.stock_info[stock].full():
                        StockInfo.stock_info[stock].get()

                    tweet_sentiment = self.tc.get_tweet_sentiment(message['body'])
                    MyLogger.dwrite(message['body'], str(tweet_sentiment))

                    StockInfo.stock_info[stock].put((message['created_at'],
                                                   tweet_sentiment,
                                                   message['body']))

            # Rate limit is 400 requests per hour = 1/9 requests per second
            t.sleep(10)

    def isDup(self, q:PriorityQueue, text):
        queue_arr = list(q.queue)
        for data in queue_arr:
            if data == text:
                return True
        return False