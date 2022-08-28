import sys


def prices_of_stocks(company):
    COMPANIES = {
'Apple': 'AAPL',
'Microsoft': 'MSFT',
'Netflix': 'NFLX',
'Tesla': 'TSLA',
'Nokia': 'NOK'
    }
    STOCKS = {
'AAPL': 287.73,
'MSFT': 173.79,
'NFLX': 416.90,
'TSLA': 724.88,
'NOK': 3.37
    }

    if company not in COMPANIES:
        return 'Unknown company'
    return STOCKS[COMPANIES[company]]


if __name__ == '__main__':
    if len(sys.argv) == 2:
        name = sys.argv[1].capitalize()
        print(prices_of_stocks(name))
    # else:
    #     print('usage: python3 stock_prices.py company')