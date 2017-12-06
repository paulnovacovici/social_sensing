import requests
import MyLogger

# StockTwits details
ST_BASE_URL = 'https://api.stocktwits.com/api/2/'
ST_BASE_PARAMS = dict(access_token='d5d9252e919908f5c34f66bbff95db50460ee325')

""" 
Uses `requests` library to GET to Stocktwits, and also to convert resonses to JSON
"""
def get_json(url, params=None):
    resp = None

    # Try to do get request 4 times otherwise fail
    for i in range(4):
        try:
            resp = requests.get(url, params=params, timeout=5)
        except requests.Timeout:
            trimmed_params = {k: v for k, v in params.iteritems() if k not in ST_BASE_PARAMS.keys()}
            MyLogger.ewrite('GET Timeout to {} w/ {}'.format(url[len(ST_BASE_URL):], trimmed_params))

        if resp is not None:
            break

    if resp is None:
        MyLogger.ewrite('GET loop Timeout')
        return None
    else:
        return resp.json()


""" 
Uses `requests` library to POST to Stocktwits, and also to convert resonses to JSON
"""
def post_json(url, params=None, deadline=30):
    resp = None
    for i in range(4):
        try:
            resp = requests.post(url, params=params, timeout=5)
        except requests.Timeout:
            trimmed_params = {k: v for k, v in params.iteritems() if k not in ST_BASE_PARAMS.keys()}
            MyLogger.ewrite('POST Timeout to {} w/ {}'.format(url[len(ST_BASE_URL):], trimmed_params))

        if resp is not None:
            break

    if resp is None:
        MyLogger.ewrite('GET loop Timeout')
        return None
    else:
        return resp.json()