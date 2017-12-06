from Requests import ST_BASE_PARAMS, ST_BASE_URL
import Requests as R

"""
Returns all messages for each symbol
"""
def get_stock_streams(symbols):
    all_params = ST_BASE_PARAMS.copy()
    all_params['symbols'] = ''
    for symbol in symbols:
        all_params['symbols'] += symbol + ','
    return R.get_json(ST_BASE_URL + 'streams/symbols.json', params = all_params)

""" 
returns list of trending stock symbols, ensuring each symbol is part of a NYSE or NASDAQ
"""
def get_trending_stocks():
    trending = R.get_json(ST_BASE_URL + 'trending/symbols.json', params=ST_BASE_PARAMS)['symbols']

    symbols = [s['symbol'] for s in trending[:10]]
    return symbols

