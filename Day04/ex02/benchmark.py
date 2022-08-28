import sys
import timeit


def filter_gmail_loop(emails):
    gmails = []
    for email in emails:
        if email.endswith('@gmail.com'):
            gmails.append(email)
    return gmails


def filter_gmail_list_comprehension(emails):
    return [email for email in emails if email.endswith('@gmail.com')]

def filter_gmail_map(emails):
    return list(map(lambda x: x if x.endswith('@gmail.com') else None, emails))

def filter_gmail_filter(emails):
    return list(filter(lambda x: x.endswith('@gmail.com'), emails))

def main(function, number):
    try:
        number = int(number)
    except:
        raise ValueError('invalid number')
    functions = {'loop', 'list_comprehension', 'map', 'filter'}
    if function not in functions:
        raise ValueError('invalid function name')
    setup = f"""
from __main__ import filter_gmail_{function}
emails = 5 * ['john@gmail.com', 'james@gmail.com',
'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    """
    stmt_1 = f'filter_gmail_{function}(emails)'
    time_g = timeit.timeit(setup=setup, stmt=stmt_1, number=number)
    return time_g


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(main(sys.argv[1], sys.argv[2]))
    else:
        print('usage: python3 benchmark.py function number')