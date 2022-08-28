import sys
import time
from bs4 import BeautifulSoup
# from urllib.request import urlopen, Request
import ssl
import urllib.parse
import urllib.request

def get_row(ticker, row):
    url = f'https://finance.yahoo.com/quote/{ticker}/financials'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    values = {'name': 'Michael Foord',
            'location': 'Northampton',
            'language': 'Python' }
    headers = {'User-Agent': user_agent}

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    # header = urllib.parse.urlencode(headers['User-Agent'])
    # header['User-Agent'] = header.encode('ascii')
# создание объекта Request с указанием, в качестве 
# аргументов, параметров запроса и заголовков
    req = urllib.request.Request(url, data, headers)
# отправка POST запроса
    try:
        with urllib.request.urlopen(req) as response:
            page = response.read()
    except:
        raise ValueError('HTTP Error 404: Not Found')
    # ssl._create_default_https_context = ssl._create_unverified_context
    # url = f'https://finance.yahoo.com/quote/{ticker}/financials'
    # try:
        # page = urlopen(Request(url=url)).read()
    # except:
        # raise ValueError('HTTP Error 404: Not Found')
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