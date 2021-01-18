from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

import api


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


def stock_card(stocks, key):
    positive = True
    grid = Table.grid(expand=False)
    grid.add_column(width=12, justify="center", header_style="cyan")
    grid.add_column(width=12, justify="center")
    grid.add_column(width=12, justify="center")
    grid.add_row("", " ", "")
    grid.add_row("[underline]Price", "[underline]Change", "[underline]Percent")
    symbol = stocks[key]['symbol']
    price = stocks[key]['price']
    previous = stocks[key]['previous']
    change = stocks[key]['change']
    percent = stocks[key]['percent']

    if change < 0:
        positive = False

    if positive:
        grid.add_row(f"{price}", "{:.2f}".format(change), "{:.2f}%".format(percent))
    else:
        grid.add_row(f"{price}", "[red]{:.2f}".format(change), "[red]{:.2f}%".format(percent))

    grid.add_row("", " ", "")

    return Panel(grid, title="[orchid]{}".format(symbol), style="blue")


def run(symbol_list):
    raw_symbol_data = api.fetch_symbol_data(symbol_list)
    stocks = (process_stock_data(raw_symbol_data))
    stock_style = Style(color="blue")

    print("▶")
    # for key in stocks.keys():
    #     print(stocks[key]['price'])

    stock_cards = [(stock_card(stocks, key)) for key in stocks.keys()]
    print(Columns(stock_cards))


def setup_symbols():
    symbol_list = ['AAPL', 'MSFT', 'GOOG']
    symbol_list.sort()
    return symbol_list


if __name__ == "__main__":
    s = setup_symbols()
    run(s)
