import sys
import time
import requests
from bs4 import BeautifulSoup
import pstats
from pstats import SortKey
session = requests.Session()
session.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'accept-language': 'ru',
        }

def get_row(ticker, row):
    # https_proxy = "http://203.23.104.5:80"
    url = f'https://finance.yahoo.com/quote/{ticker}/financials'
    page = session.get(url).text
    page_parsed = BeautifulSoup(page, 'html.parser')
    title = page_parsed.title.string
    if title == 'Symbol Lookup from Yahoo Finance':
        raise ValueError('ticker does not exist')
    tags = page_parsed.find_all(attrs={'data-test': 'fin-row'})
    for gg in tags:
        tag = gg.find(string=row)
        if tag == row:
            items = gg.find_all(attrs={'data-test': 'fin-col'})
            pp = [el.get_text() for el in items]
            pp.insert(0, tag)
            return tuple(pp)
    raise ValueError('row does not exist')
def main():
    if len(sys.argv) == 3:
        print(get_row(sys.argv[1], sys.argv[2]))
    else:
        print('usage: python3 financial.py ticker field')

import pstats
import profile

p = profile.Profile()
p.run("main()")

s = pstats.Stats(p)
s.sort_stats("cumtime").print_stats(5)