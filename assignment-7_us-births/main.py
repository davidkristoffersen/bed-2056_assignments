#!/usr/bin/python3
'''Us births'''

import csv


def get_data(path):
    '''Read txt file'''
    with open(path, 'r') as _f:
        for line in _f:
            yield line


def parse_data(data, idxs):
    '''Parse data'''
    for line in data:
        yield [
            int(line[idxs[0][0]:idxs[0][1]]),
            int(line[idxs[1][0]:idxs[1][1]]),
            line[idxs[2][0]:idxs[2][1]],
            int(line[idxs[3][0]:idxs[3][1]])
        ]


def write_csv(data, path):
    '''Write data to csv file'''
    with open(path, 'w', newline='') as _f:
        _wr = csv.writer(_f, quoting=csv.QUOTE_NONNUMERIC)
        _wr.writerows(data)


def read_csv(path):
    '''Read csv file'''
    with open(path, newline='') as _f:
        return list(csv.reader(_f, quoting=csv.QUOTE_NONNUMERIC))


def print_data(data):
    '''Pretty print data'''
    # headers = ['Birth month', 'Birth day of week', 'Sex', 'Weight(g)']
    headers = ['bm', 'bd', 's', 'wg']
    for _h in headers:
        print(_h, end='\t')
    print()
    for line in data:
        for _d in line:
            print(_d, end='\t')
        print()


def init_download(inpf, outf):
    '''First time txt conversion to csv'''
    idxs = [
        [13, 14],
        [23, 23],
        [475, 475],
        [504, 507],
    ]
    idxs = [[idx[0] - 1, idx[1]] for idx in idxs]

    data = get_data(inpf)
    data = parse_data(data, idxs)

    write_csv(data, outf)


def main():
    '''Main func'''
    data = read_csv('small2019.csv')
    print_data(data)


if __name__ == '__main__':
    main()
