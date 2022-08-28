import sys
import timeit
from functools import reduce


def sum_of_squares_loop(n):
    res = 0
    for i in range(1, n + 1):
        res += i ** 2
    return res


def sum_of_squares_reduce(n):
    return reduce(lambda x, y: x + y ** 2, [i for i in range(1, n + 1)])


def compute_time(function, number, n):
    try:
        number = int(number)
    except:
        raise ValueError('invalid number')
    try:
        n = int(n)
    except:
        raise ValueError('invalid sum')
    functions = {'loop', 'reduce'}
    if function not in functions:
        raise ValueError('invalid function name')
    setup = f'from __main__ import sum_of_squares_{function}'
    stmt = f'sum_of_squares_{function}({n})'
    return timeit.timeit(setup=setup, stmt=stmt, number=number)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        print(compute_time(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print('usage: python3 benchmark.py function number n')

