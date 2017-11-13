import json
import requests

def getData(ticker):
    rsp = requests.get('https://finance.google.com/finance?q=%s&output=json' % ticker)

    if rsp.status_code in (200,):
        # https://stackoverflow.com/questions/46080632/http-error-404-from-googlefinance-in-python-2-7
        fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
        return fin_data
    else:
        return None

"""
Get's last trade price for stock with ticker
@:param ticker 
"""
def getStockPrice(ticker):
    fin_data = getData(ticker)
    return fin_data['l']

"""
Get's 52 week Low for stock with ticker
"""
def get52WeekLow(ticker):
    fin_data = getData(ticker)
    return fin_data["lo52"]

"""
Get's 52 week High for stock with ticker
"""
def get52WeekHi(ticker):
    fin_data = getData(ticker)
    return fin_data["hi52"]