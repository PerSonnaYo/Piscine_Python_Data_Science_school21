
import timeit


def filter_gmail_1(emails):
    gmails = []
    for email in emails:
        if email.endswith('@gmail.com'):
            gmails.append(email)
    return gmails


def filter_gmail_2(emails):
    return [email for email in emails if email.endswith('@gmail.com')]

def filter_gmail_3(emails):
    return list(map(lambda x: x if x.endswith('@gmail.com') else None, emails))


def main():
    setup = """
from __main__ import filter_gmail_1, filter_gmail_2, filter_gmail_3
emails = 5 * ['john@gmail.com', 'james@gmail.com',
'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    """
    stmt_1 = 'filter_gmail_1(emails)'
    stmt_2 = 'filter_gmail_2(emails)'
    stmt_3 = 'filter_gmail_3(emails)'
    time_g = {timeit.timeit(setup=setup, stmt=stmt_1, number=90000000): 'loop',
 timeit.timeit(setup=setup, stmt=stmt_2, number=90000000): 'list comprehension',
 timeit.timeit(setup=setup, stmt=stmt_3, number=90000000): 'map'}

    res = time_g[min(time_g.keys())]
    time_sorted = sorted(time_g.keys())
    print(f'it is better to use a {res}')
    print(f'{time_sorted[0]} vs {time_sorted[1]} vs {time_sorted[2]}')


if __name__ == '__main__':
    main()