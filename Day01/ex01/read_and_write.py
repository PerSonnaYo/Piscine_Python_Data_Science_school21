def read_and_write(filename):
    filename1 = filename + ".csv"
    filename2 = filename + ".tsv"
    with open(filename1, 'r') as onread:
        with open(filename2, 'w') as onwrite:
            res = onread.read().replace('\",', '\"\t')
            res = res.replace('false,', 'false\t')
            res = res.replace('true,', 'true\t')
            onwrite.write(res)


if __name__ == '__main__':
    read_and_write('ds')