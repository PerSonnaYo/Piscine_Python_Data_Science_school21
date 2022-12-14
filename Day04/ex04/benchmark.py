import timeit
import random
from collections import Counter


def my_func(elems):
    counter = dict()
    for elem in elems:
        if elem not in counter:
            counter[elem] = 0
        counter[elem] += 1
    return counter


def my_top(elems, n):
    counter = my_func(elems)
    return sorted(counter.items(), key=lambda x: -x[1])[:n]

def main():
    setup = """
import random
from collections import Counter
from __main__ import my_func, my_top
random.seed(5)
elems = [random.randint(0, 100) for i in range(1000000)]
    """
    time_1 = timeit.timeit(setup=setup, stmt='my_func(elems)', number=10)
    time_2 = timeit.timeit(setup=setup, stmt='Counter(elems)', number=10)
    time_3 = timeit.timeit(setup=setup, stmt='my_top(elems, 10)', number=10)
    time_4 = timeit.timeit(setup=setup, stmt='Counter(elems).most_common(10)', number=10)
    print(f"my function: {time_1}")
    print(f"Counter: {time_2}")
    print(f"my top: {time_3}")
    print(f"Counter's top: {time_4}")


if __name__ == '__main__':
    main()

