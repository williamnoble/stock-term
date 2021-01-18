import yaml


# configuration = {
#     "watchlist": [],
#     "positions": {
#         "stock": ["", "", ""]
#     },
# }
#

def get_config():
    watchlist = []
    positions = {}
    with open('config.yaml') as f:
        docs = yaml.load_all(f, Loader=yaml.FullLoader)

        for doc in docs:
            watchlist = list(stock for stock in doc["watchlist"])

        for pos, value in doc["positions"].items():
            positions[pos] = value
            # print("pos: ", pos,
            #       "val: ", value,
            #       "d: \n", doc["positions"][pos])

        # print("Wills Watchlist ", watchlist)
        # print("Wills Positions", positions)
        return watchlist, positions
#
# mock_configuration = {
#     "watchlist": ["AAPL, MSFT", "GOOG"],
#     "positions": {
#         "AAPL": ["01/01/2020 213.01 23", "02/03/2020 213.02 45", "03/04/2020 217.38"],
#         "MSFT": ["01/02/2020 22.93 03", "03/07/2020 56.12 74", "06/09/2020 64.23 17"],
#     },
# }
