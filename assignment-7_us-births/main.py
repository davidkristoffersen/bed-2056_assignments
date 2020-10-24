#!/usr/bin/python3
'''Us births'''

import csv
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt


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


def zero_month():
    '''Gen zero month'''
    return [0 for i in range(12)]


def zero_day():
    '''Gen zero day'''
    return [0 for i in range(7)]


def count_data(data):
    '''Count up data'''
    sex_data = [zero_month(), zero_month()]
    weight_data = [[zero_month(), zero_month()], [zero_month(), zero_month()]]
    day_data = [zero_day(), zero_day()]
    sex_map = {'M': 0, 'F': 1}

    for line in data:
        sex = sex_map[line[2]]
        month = int(line[0]) - 1
        day = int(line[1]) - 1

        sex_data[sex][month] += 1
        weight_data[sex][0][month] += line[3]
        weight_data[sex][1][month] += 1
        day_data[sex][day] += 1

    for sex in weight_data:
        for i in range(12):
            if sex[1][i]:
                sex[0][i] = int(sex[0][i] / sex[1][i])
    weight_data[0] = weight_data[0][0]
    weight_data[1] = weight_data[1][0]

    return {
        'sex': [[i + 1 for i in range(12)], sex_data, [i + 1 for i in range(0, 12, 2)]],
        'Mean weight': [[i + 1 for i in range(12)], weight_data, [i + 1 for i in range(0, 12, 2)]],
        'Week day': [[i + 1 for i in range(7)], day_data, [i + 1 for i in range(7)]]
    }


def plot_graphs(data2017, data2018, data2019):
    '''Plot all years data'''
    cols = 3
    rows = 3

    fig, axes = plt.subplots(rows, cols)
    axes[0][0].set_ylabel('2017', labelpad=20, rotation=0, size='large')
    axes[1][0].set_ylabel('2018', labelpad=20, rotation=0, size='large')
    axes[2][0].set_ylabel('2019', labelpad=20, rotation=0, size='large')

    axes[2][0].set_xlabel('Month', size='large')
    axes[2][1].set_xlabel('Month', size='large')
    axes[2][2].set_xlabel('Week day', size='large')

    for i, (key, val) in enumerate(data2017.items()):
        _y = int(i % cols)
        axes[0][_y].plot(val[0], val[1][0], c="orange")
        axes[0][_y].plot(val[0], val[1][1], c="cyan")
        axes[1][_y].plot(data2018[key][0], data2018[key][1][0], c="orange")
        axes[1][_y].plot(data2018[key][0], data2018[key][1][1], c="cyan")
        axes[2][_y].plot(data2019[key][0], data2019[key][1][0], c="orange")
        axes[2][_y].plot(data2019[key][0], data2019[key][1][1], c="cyan")
        axes[0][_y].set_title(key)
        axes[0][_y].set_xticks(val[2])
        axes[1][_y].set_xticks(val[2])
        axes[2][_y].set_xticks(val[2])

    fig.add_subplot(111, frame_on=False)
    fig.tight_layout()
    plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)

    legend_handles = [Line2D([0], [0], color="orange", lw=2, label="Male"),
                      Line2D([0], [0], color="cyan", lw=2, label="Female")]
    plt.legend(handles=legend_handles, loc="upper left")

    plt.suptitle("US birth rates", fontweight="bold")

    plt.savefig("output.pdf")


def main():
    '''Main func'''
    file_type = 'data'
    files = [file_type + str(x) + '.csv' for x in range(2017, 2020)]
    data = [read_csv(_f) for _f in files]
    data = [count_data(_d) for _d in data]
    plot_graphs(*data)


if __name__ == '__main__':
    main()
