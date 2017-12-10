import json

from queue import PriorityQueue
from tweepy import StreamListener

import MyLogger


class StdOutListener(StreamListener):

    def __init__(self, tc, trending, stock_tweets):
        super().__init__()
        self.tc = tc
        self.trending = trending
        self.stock_tweets = stock_tweets

    def on_data(self, data):
        # Check what ticker symbol the data is about and push to queue
        tweet = json.loads(data)

        for stock in self.trending:
            if stock in tweet['text']:
                if stock not in self.stock_tweets:
                    self.stock_tweets[stock] = PriorityQueue(maxsize=50)
                elif self.isDup(self.stock_tweets[stock], tweet['text']):
                    continue

                if self.stock_tweets[stock].full():
                    self.stock_tweets[stock].get()

                tweet_sentiment = self.tc.get_tweet_sentiment(tweet['text'])
                MyLogger.dwrite(tweet['text'], str(tweet_sentiment))

                self.stock_tweets[stock].put((tweet['created_at'], tweet_sentiment , tweet['text']))
        return True

    def isDup(self, q:PriorityQueue, text):
        queue_arr = list(q.queue)
        for data in queue_arr:
            if data == text:
                return True
        return False

    def on_error(self, status):
        with open('listener.log', 'w') as f:
            f.write(status)