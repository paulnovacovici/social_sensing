import os
from datetime import datetime

DEBUG = False
log = open(os.path.dirname(os.path.abspath(__file__)) + 'website/purchase_log.txt', 'a',1)
elog = open(os.path.dirname(os.path.abspath(__file__)) + '/elog.txt', 'a',1)
dlog = open(os.path.dirname(os.path.abspath(__file__)) + '/dlog.txt', 'a',1)

def write(text):
    global log
    log.write(str(datetime.now()) + "\t" + text + '\n')

def ewrite(text):
    global elog
    elog.write(str(datetime.now()) + "\t" + text + '\n')

def dwrite(text, sentiment=None):
    global dlog
    if DEBUG:
        try:
            dlog.write(str(datetime.now()) + "\n" + text + '\n')
        except UnicodeEncodeError:
            pass
        if sentiment is not None:
            dlog.write("Sentiment: " + sentiment + '\n')

def clear():
    global log
    log.close()
    log = open(os.path.dirname(os.path.abspath(__file__)) + '/log.txt', 'w',1)