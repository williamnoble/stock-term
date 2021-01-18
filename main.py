from rich import print
from rich.columns import Columns
import ui
import api
import yaml
import config as c


def process_stock_data(raw_symbol_data):
    stocks = {}
    price, change, percent = None, None, None
    for result in raw_symbol_data['quoteResponse']['result']:
        market_key = "default"
        if result['marketState'] == 'POST' and \
                result['postMarketChange'] is not None and result[
            'postMarketChange'] != 0:
            market_key = "post"
        elif result['marketState'] == 'PRE' and \
                result['preMarketChange'] is not None and result[
            'preMarketChange'] != 0:
            market_key = "pre"
        else:
            market_key = "default"

        symbol = result['symbol']
        if market_key == "default":
            price = result['regularMarketPrice']
            change = result['regularMarketChange']
            percent = result['regularMarketChangePercent']
        elif market_key == "post":
            price = result['postMarketPrice']
            change = result['postMarketChange']
            percent = result['postMarketPercentagePercent']
        elif market_key == "pre":
            price = result['preMarketPrice']
            change = result['preMarketChange']
            percent = result['postMarketChangePercent']

        stock = {
            "symbol": symbol,
            "price": price,
            "previous": result['regularMarketPreviousClose'],
            "change": change,
            "percent": percent,
            "qualifier": market_key

        }
        stocks[symbol] = stock

    return stocks


def run(symbol_list, stock_watchlist, stock_positions):
    raw_symbol_data = api.fetch_symbol_data(symbol_list)
    stocks = (process_stock_data(raw_symbol_data))
    adjusted_set = set()
    # for key in stocks.keys():
    #     print(stocks[key]['price'])
    stock_cards = [(ui.stock_card(stocks, key, stock_watchlist, stock_positions, adjusted_set)) for key in stocks.keys()]
    print(Columns(stock_cards, padding=(2, 0, 0, 0)))


def setup_symbols(symbol_list):
    # symbol_list.sort()
    # return symbol_list
    symbol_list.sort()
    return symbol_list


if __name__ == "__main__":
    import os

    # watchlist = ['AAPL', 'MSFT', 'GOOG', 'TSLA', 'F', 'KO']
    os.system('cls' if os.name == 'nt' else 'clear')

    watchlist, positions = c.get_config()
    # print(positions)
    s = setup_symbols(watchlist)

    run(s, watchlist, positions)
    print("\n\nStock Term version: 0.1 by William Noble\n\n")
