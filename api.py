import http.client
import json
import os

import const as c


# API_ENDPOINT = 'query1.finance.yahoo.com'
# API_PATH = '/v7/finance/quote'

def fetch_symbol_data(symbols):
    conn = http.client.HTTPSConnection(c.API_ENDPOINT, timeout=1)
    try:
        conn.request('GET', c.API_PATH + '?symbols=' + ','.join(symbols) + '&fields=' + c.API_FIELDS)
        resp = conn.getresponse()
        if resp.status != 200:
            print("error in retrieving symbol data")
            exit(-1)

    except:
        print("exception generated when trying to get stock data")
        exit(-1)

    return json.loads(resp.read().decode())
