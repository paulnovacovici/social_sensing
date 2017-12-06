import time

import MyLogger
from Scraper import Scraper

if __name__ == "__main__":
    # For testing purposes create a trending array
    MyLogger.DEBUG = True
    trending = ["AMD", "MSFT", "GOOG", "AAPL", "TSLA"]
    scraper = Scraper(trending)