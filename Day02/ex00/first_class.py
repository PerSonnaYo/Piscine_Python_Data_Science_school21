class Must_read():
    with open('data.csv', "r") as data:
        print(data.read())

if __name__ == '__main__':
    x = Must_read()