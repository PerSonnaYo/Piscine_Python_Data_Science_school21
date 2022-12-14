import sys


def ticker_symbols(ticker):
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

    tickers = {}
    for com in COMPANIES:
        tickers[COMPANIES[com]] = com 
    if ticker not in tickers:
        return 'Unknown ticker'
    return f'{tickers[ticker]} {STOCKS[ticker]}'


if __name__ == '__main__':
    if len(sys.argv) == 2:
        name = sys.argv[1].upper()
        print(ticker_symbols(name))
    # else:
    #     print('usage: python3 ticker_symbols.py ticker')