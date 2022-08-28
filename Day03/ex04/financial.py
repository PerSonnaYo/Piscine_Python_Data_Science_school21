import sys
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import ssl

def get_row(ticker, row):
    ssl._create_default_https_context = ssl._create_unverified_context
    url = f'https://finance.yahoo.com/quote/{ticker}/financials'
    page = urlopen(Request(url=url)).read()
    time.sleep(5)
    # time.sleep(5)
    page_parsed = BeautifulSoup(page, "html.parser")
    title = page.title
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


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(get_row(sys.argv[1], sys.argv[2]))
    else:
        print('usage: python3 financial.py ticker field')