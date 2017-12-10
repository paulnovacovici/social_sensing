from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from queue import PriorityQueue
from StdOutListener import StdOutListener

import json
import tweepy
import re
import MyLogger
import StockInfo


class TwitterClient(object):
    def __init__(self):
        self.stream = None
        # Variables that contains the user credentials to access Twitter API

        access_token = "1518310573-wZ4sDaFpEUXjSev2QMxl4WW4WN4fzl94qGm7UF9"
        access_token_secret = "esP6wEjyEzYBQdhWxls0tIFB0DFc25zOyy98Kb27No19e"
        consumer_key = "M9Z2tc3gY05m9a67IsfAGEdQp"
        consumer_secret = "DRcVhwFzMAFK7ZRKFVuPE8o4SIRrMiLWRRvFWJu4x5wcD5IKoM"

        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            MyLogger.ewrite("Authentication Failed!")

    """
    Removes unwanted characters in the sentiment api
    @:param tweet that needs to be cleaned
    """
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    """
    Increases modularity so in the future can test different
    api's such as IBM Watson's
    @:param text to analyze
    """
    def sentiment_api(self, text):
        return TextBlob(self.clean_tweet(text))

    """
    Wrapper of sentiment api to return a positive or negative result
    @:param tweet to analyze
    """
    def get_tweet_sentiment(self, tweet):
        analysis = self.sentiment_api(tweet)

        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            #TODO: What to do when sentiment api can't distinguish?
            return 0
        else:
            return 0

    """
    Starts stream of real time tweets
    @:param trending array of tickers
    """
    def get_tweets_stream(self, trending):
        l = StdOutListener(self, trending, StockInfo.stock_info)
        self.stream = Stream(self.api.auth, l)
        self.stream.filter(track=['$' + stock for stock in trending],async=True)

    def close_stream(self):
        if self.stream is not None:
            self.stream.disconnect()

    """
    Fetches a certian amount of tweets from rest api
    @:param query 
    @:param count number of tweets 
    """
    def get_tweets_rest(self, query, count=30):
        ticker = query[1:]
        if ticker not in StockInfo.stock_info:
            StockInfo.stock_info[ticker] = PriorityQueue(maxsize=50)

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                tweet_sent = self.get_tweet_sentiment(tweet.text)

                tweet = json.loads(json.dumps(tweet._json))
                # TODO: In future check if tweet is already in queue
                if StockInfo.stock_info[query].full():
                    StockInfo.stock_info[query].get()
                StockInfo.stock_info[query].put((tweet['created_at'], tweet_sent == 'positive', tweet['text']))

        except tweepy.TweepError as e:
            MyLogger.ewrite("Error : " + str(e))
