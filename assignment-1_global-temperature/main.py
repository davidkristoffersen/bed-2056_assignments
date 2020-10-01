#!/usr/bin/env python3

from statistics import mean
from matplotlib import pyplot as plt
from urllib.request import urlopen

# Number of lines to remove from the import files
bottom_strip_lines = 13
# Output graph file name
out_file = 'plot.pdf'


# Helper function to print imported ssv files
def print_lines(lines):
    for line in lines:
        print(line)


# Get file by url
def get_file(url):
    with urlopen(url) as f:
        return f.read().decode('utf-8')


# Parse out year and global column from file
def parse_file(f):
    lines = [' '.join(line.split()) for line in f.split('\n')]
    lines = lines[1:-1 * bottom_strip_lines]
    ret = [
        [data for it, data in enumerate(line.split(' ')) if it in [0, 2]]
        for line in lines
    ]
    ret = [[data[0], float(data[1])] for data in ret if int(data[0]) >= 1980]
    return ret


# Generate mean from data lists
def gen_mean(datas):
    ret = [[], []]
    it = 0
    for data in datas:
        if it == 12:
            it = 0
        if not it:
            ret[0].append(data[0])
            ret[1].append([])
        ret[1][-1].append(data[1])
        it += 1
    return [ret[0], [float('{:.4f}'.format(mean(data))) for data in ret[1]]]


# Plot graph
def plot(x, loc_list):
    # Init plot vars
    labels = []
    fig = plt.figure()
    ax = fig.add_subplot()

    # Convert data to plot axises
    for loc in loc_list:
        y = loc['data'][1]
        ax.plot(x, y, linewidth=loc['plot']['width'], linestyle=loc['plot']['style'])
        labels.append(loc['plot']['name'])

    # Generate legend
    plt.legend(labels, loc='upper right')
    # Set labels and title
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    fig.suptitle('Global temperature development')
    ax.set_title('Right aligned mean in the period 1980-2020')

    # Fix date format of x axis
    fig.autofmt_xdate()
    # Only show every third year
    for it, label in enumerate(ax.get_xaxis().get_ticklabels()):
        if it % 3:
            label.set_visible(False)

    plt.savefig(out_file)


if __name__ == '__main__':
    # List of all locations
    locations = [
        {
            'data': 'https://www.nsstc.uah.edu/data/msu/v6.0/tlt/uahncdc_lt_6.0.txt',
            'plot': {
                'name': 'Lower troposphere',
                'style': '-',
                'width': 1
            }
        },
        {
            'data': 'https://www.nsstc.uah.edu/data/msu/v6.0/tmt/uahncdc_mt_6.0.txt',
            'plot': {
                'name': 'Mid troposphere',
                'style': '-',
                'width': 1
            }
        },
        {
            'data': 'https://www.nsstc.uah.edu/data/msu/v6.0/ttp/uahncdc_tp_6.0.txt',
            'plot': {
                'name': 'Tropopause',
                'style': '-',
                'width': 1
            }
        },
        {
            'data': 'https://www.nsstc.uah.edu/data/msu/v6.0/tls/uahncdc_ls_6.0.txt',
            'plot': {
                'name': 'Lower stratosphere',
                'style': '-',
                'width': 1
            }
        }
    ]

    # Convert location url to right aligned mean list
    for loc in locations:
        f = get_file(loc['data'])
        data = parse_file(f)
        loc['data'] = gen_mean(data)

    # Get common year list
    years = locations[0]['data'][0]

    # Generate average of all locations
    average = []
    for loc in locations[:-1]:
        average.append(loc['data'][1])
    average = [float('{:.4f}'.format(mean(data))) for data in zip(*average)]
    locations.append({
        'data': [years, average],
        'plot': {
            'name': 'Average',
            'style': '--',
            'width': 2
        }
    })

    # Plot graph
    plot(years, locations)
