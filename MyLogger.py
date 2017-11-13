import os
from datetime import datetime

class MyLogger(object):
    log = open(os.path.dirname(os.path.abspath(__file__)) + '/log.txt', 'a',1)

    def write(self,text):
        MyLogger.log.write(str(datetime.now()) + "\t" + text + '\n')

    def clear(self):
        MyLogger.log.close()
        MyLogger.log = open(os.path.dirname(os.path.abspath(__file__)) + '/log.txt', 'w',1)