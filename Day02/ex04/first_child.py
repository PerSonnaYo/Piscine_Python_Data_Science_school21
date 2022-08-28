import sys
from random import randint

class Research():
    def __init__(self, filename):
        self.filename = filename
        self.data = self.file_reader()
        self.calc = self.Analytics(self.data)

    def file_reader(self, has_header=True):
        with open(self.filename, 'r') as file:
            text = file.read()
        lines = text.split('\n')
        new_lines = [line  for line in lines if line != '']
        if has_header and len(new_lines[0].split(',')) != 2:
            raise ValueError('Incorrect header')
        y = 0
        if has_header:
            y = 1
        if len(new_lines) == 0:
            raise ValueError('No lines')
        for i in range(y, len(new_lines)):
            if new_lines[i] != '1,0' and new_lines[i] != '0,1':
                raise ValueError('Incorrect line')
        return [[int(elem) for elem in new_lines[i].split(',')] for i in range(y, len(new_lines))]

    class Calculations():
        def __init__(self, data):
            self.data = data

        def counts(self):
            res = []
            for elem in zip(*self.data):
                res.append(str(sum(elem)))
            return (" ".join(res))

        def fractions(self, count):
            count = list(map(int, count.split(' ')))
            res = []
            for elem in count:
                res.append(str(elem / sum(count) * 100))
            return " ".join(res)

    class Analytics(Calculations):
        def predict_random(self, num_steps):
            dictionary = {0: [0, 1], 1: [1, 0]}
            return [dictionary[randint(0, 1)] for i in range(num_steps)]
        def predict_last(self):
            return self.data[-1]


if __name__ == '__main__':
    if len(sys.argv) == 2:
        r = Research(sys.argv[1])
        counts = r.calc.counts()
        fract = r.calc.fractions(counts)
        print(r.data)
        print(counts)
        print(fract)
        print(r.calc.predict_random(3))
        print(r.calc.predict_last())
    else:
        print('usage: python3 first_constructor.py filepath')