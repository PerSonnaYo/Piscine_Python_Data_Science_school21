
import sys


class Research():
    def __init__(self, filename):
        self.filename = filename
        self.calc = self.Calculations()

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
        # print(new_lines)
        for i in range(y, len(new_lines)):
            if new_lines[i] != '1,0' and new_lines[i] != '0,1':
                raise ValueError('Incorrect line')
        return [[int(elem) for elem in new_lines[i].split(',')] for i in range(y, len(new_lines))]

    class Calculations():
        def counts(self, data):
            res = []
            for elem in zip(*data):
                res.append(str(sum(elem)))
            return (" ".join(res))

        def fractions(self, count):
            count = list(map(int, count.split(' ')))
            res = []
            for elem in count:
                res.append(str(elem / sum(count) * 100))
            return " ".join(res)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        r = Research(sys.argv[1])
        data = r.file_reader()
        counts = r.calc.counts(data)
        fract = r.calc.fractions(counts)
        print(data)
        print(counts)
        print(fract)
    else:
        print('usage: python3 first_constructor.py filepath')