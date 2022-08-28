import sys
# https://dvsemenov.ru/shifr-cezarya-na-python-rukovodstvo-po-shifrovaniyu-teksta/

def encode_function(string, shift):
    res = ''
    ascii_lowercase = (''.join([chr(i) for i in range(97,123)]))
    ascii_uppercase = (''.join([chr(i) for i in range(65,91)]))
    printable = set( ascii_lowercase + ascii_uppercase + '0123456789' +
        r'!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~' + ' \t\n\r\f\v')
    for char in string:
        if char not in printable:
            raise ValueError(' The script does not support your language yet')
        elif char in ascii_lowercase:
            idx = ascii_lowercase.find(char)
            res += ascii_lowercase[(idx + shift) % 26]
        elif char in ascii_uppercase:
            idx = ascii_uppercase.find(char)
            res += ascii_uppercase[(idx + shift) % 26]
        else:
            res += char
    return res


if __name__ == '__main__':
    if len(sys.argv) == 4:
        if sys.argv[1] == 'decode':
            print(encode_function(sys.argv[2], -int(sys.argv[3])))
        elif sys.argv[1] == 'encode':
            print(encode_function(sys.argv[2], int(sys.argv[3])))
        else:
            raise ValueError('Incorrect option')
    else:
        raise ValueError('Incorrect number of arguments')