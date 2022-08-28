import sys


# def find_element(elem):
#     companies = {
#         'Apple': 'AAPL',
#         'Microsoft': 'MSFT',
#         'Netflix': 'NFLX',
#         'Tesla': 'TSLA',
#         'Nokia': 'NOK'
#         }
#     tickers = {value: key for key, value in companies.items()}
#     stocks = {
#         'AAPL': 287.73,
#         'MSFT': 173.79,
#         'NFLX': 416.90,
#         'TSLA': 724.88,
#         'NOK': 3.37
#         }
#     elem_cap = elem.capitalize()
#     elem_up = elem.upper()
#     if elem_cap in companies:
#         return f'{elem_cap} stock price is {stocks[companies[elem_cap]]}'
#     elif elem_up in tickers:
#         return f'{elem_up} is a ticker symbol for {tickers[elem_up]}'
#     return f'{elem} is an unknown company or an unknown ticker symbol'


# def all_stocks(string):
#     string_split = string.replace(',', ' , ').split()
#     commas_num = string_split.count(',')
#     if commas_num * 2 + 1 == len(string_split):
#         for elem in string_split:
#             if elem != ',':
#                 print(find_element(elem.strip(',')))


# if __name__ == '__main__':
#     if len(sys.argv) == 2:
#         all_stocks(sys.argv[1])
#     else:
#         print('usage: python3 all_stocks.py string')

#TODO разделяются только запятыми
def all_stocks(items):
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
    stocks = {
        'MSFT': 173.79,
        'TSLA': 724.88,
        'NFLX': 416.90,
        'AAPL': 287.73,
        'NOK': 3.37
        }
    varibles = items.split(',')
    comp = []
    for el in varibles:
        sel = el.replace(' ', '')
        if sel == '' or sel is None:
            return
        comp.append(sel)
    for com in comp:
        name1 = com.capitalize()
        name2 = com.upper()
        if name1 in COMPANIES:
            print (f'{name1} stock price is {stocks[COMPANIES[name1]]}')
        elif name2 in tickers:
            print( f'{name2} is a ticker symbol for {tickers[name2]}')
        else:
            print( f'{com} is an unknown company or an unknown ticker symbol')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        all_stocks(sys.argv[1])
    # else:
    #     print('usage: python3 ticker_symbols.py ticker')