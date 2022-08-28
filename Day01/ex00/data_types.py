def data_types():
    var = [1, '', 1.0, True, [], {}, (), set()]
    print([type(el).__name__ for el in var])


if __name__ == '__main__':
    data_types()