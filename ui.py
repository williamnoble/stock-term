from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style

PROFIT = 124
MAX_WIDTH = "36"

NEG_PRICE = Style(
    color="red"
)

POS_PRICE = Style(
    color="default"
)


def card_overview(master_grid, positive, stocks, key):
    symbol = stocks[key]['symbol']
    price = stocks[key]['price']
    previous = stocks[key]['previous']
    change = stocks[key]['change']
    adjusted_change = "{:.2f}".format(change)
    percent = stocks[key]['percent']
    adjusted_percent = "{:.2f}%".format(percent)
    grid = Table.grid(expand=False)
    if change < 0:
        positive = False
    grid.add_column(width=18, justify="left")
    grid.add_column(width=18, justify="right")
    grid.add_row(f"Price", f"${price}\r")
    grid.add_row(f"Prev Close", f"[underline]${previous}\r", style="dim")
    grid.add_row("", f"{adjusted_change}", style=POS_PRICE if positive else NEG_PRICE)
    grid.add_row("", f"{adjusted_percent}", style=POS_PRICE if positive else NEG_PRICE)
    return grid


def card_price_grid(master_grid, positive, stocks, key, positions, position_adjustment, total_profit):
    price_grid = Table.grid(expand=False)
    table = Table(show_header=True,
                  box=box.SIMPLE,
                  show_lines=False,
                  show_edge=False,
                  row_styles=["none", "dim"],
                  padding=0,
                  )

    # ADD STOCK COLUMNS
    table.add_column("", width=2, justify="left")
    table.add_column("[green]date", justify="left", style="green", width=14)
    table.add_column("[yellow]price", justify="right", style="yellow", width=10)
    table.add_column("[blue]diff", justify="right", style="blue", width=10)
    # ADD STOCK DATA

    for k in positions:
        n_pos = 0
        total_profit[k] = 0
        found = False
        if k == key:
            found = True

            position_adjustment.add(k)
            for pos in positions[k]:
                # table.add_row("*", "++", "", "")
                p_date = positions[k][n_pos].split()[0]
                p_price = positions[k][n_pos].split()[1]
                p_amount = positions[k][n_pos].split()[2]
                actual_profit = float(stocks[key]['price']) - float(p_price)
                total_profit[k] += (actual_profit * float(p_amount))
                table.add_row(":arrow_forward:", f"{p_date}", f"{p_price}", "{:.2f}".format(actual_profit))
                # print(positions[k][0])
                n_pos += 1
            for i in range(5 - n_pos):
                table.add_row(":arrow_forward:", "--", "--", "--")
    if key not in position_adjustment:
        for i in range(5):
            table.add_row(":arrow_forward:", "--", "--", "--")
    # table.add_row(":arrow_forward:", "03/07/2020", "124.56", "+$21.34")
    # table.add_row(":arrow_forward:", "21/11/2020", "$178.45", "+$81.24")
    # table.add_row(":arrow_forward:", "12/12/2020", "$179.47", "+$82.23")
    # table.add_row(":arrow_forward:", "12/12/2020", "$179.47", "+$82.23")
    # table.add_row(":arrow_forward:[yellow]*", "12/12/2020", "$179.47", "+$82.23")
    price_grid.add_row(table)
    return price_grid


def card_footer(master_grid, profit, key):
    p = profit.get(key, 0.00)
    profit_to_date = "Profit to date: ${:.2f}".format(p)
    text_profit = Text(profit_to_date, justify="center", style="bold magenta")
    master_grid.add_row("")
    master_grid.add_row(text_profit)
    # master_grid.add_row(ColorBox())


def stock_card(stocks, key, watchlist, positions, adjusted):
    profit = {}
    positive = True
    symbol = stocks[key]['symbol']
    master_grid = Table.grid(expand=False)
    master_grid.add_column(36)
    master_grid.add_row("")

    overview = card_overview(master_grid, positive, stocks, key)
    price_grid = card_price_grid(master_grid, positive, stocks, key, positions, adjusted, profit)

    # master_grid.add_row(":arrow_forward: Price Data")
    master_grid.add_row("")
    master_grid.add_row(overview)
    master_grid.add_row("")
    master_grid.add_row("")
    master_grid.add_row(price_grid)

    card_footer(master_grid, profit, key)

    title = Text("- {} -".format(symbol))
    return Panel(master_grid, title=title, box=box.SIMPLE, style="bold magenta")
