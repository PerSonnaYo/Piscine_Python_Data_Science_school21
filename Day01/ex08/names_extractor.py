import sys

def names_extractor(filename):
    with open(filename, 'r') as input:
        with open('employees.tsv', 'w') as output:
            output.write('Name\tSurname\tE-mail\n')
            for line in input:
                buf = line.split('@')[0].split('.')
                name = buf[0].capitalize()
                surname = buf[1].capitalize()
                output.write(f'{name}\t{surname}\t{line}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        names_extractor(sys.argv[1])
    else:
        print('usage: python3 names_extractor.py filename')