class Research():
    def file_reader(self):
        with open('data.csv', 'r') as data:
            text = data.read()
        return text


if __name__ == '__main__':
    print(Research().file_reader())