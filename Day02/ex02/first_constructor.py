import sys


class Research():
    def __init__(self, filename):
        self.filename = filename

    def file_reader(self):
        with open(self.filename, 'r') as file:
            text = file.read()
        lines = text.split('\n')
        new_lines = [line  for line in lines if line != '']
        if len(new_lines) < 2:
            raise ValueError('Too few lines')
        if len(new_lines[0].split(',')) != 2:
            raise ValueError('Incorrect header')
        for i in range(1, len(new_lines)):
            if new_lines[i] != '1,0' and new_lines[i] != '0,1':
                raise ValueError('Incorrect line')
        return text


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(Research(sys.argv[1]).file_reader())
    else:
        print('usage: python3 first_constructor.py filepath')