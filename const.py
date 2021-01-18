API_ENDPOINT = 'query1.finance.yahoo.com'
API_PATH = '/v7/finance/quote'
API_FIELDS = ','.join([
    'symbol',
    'marketState',
    'regularMarketPrice',
    'regularMarketChange',
    'regularMarketChangePercent',
    'preMarketPrice',
    'preMarketChange',
    'preMarketChangePercent',
    'postMarketPrice',
    'postMarketChange',
    'postMarketChangePercent'
])