#!/usr/bin/python3
"""Bankcrypties based on covid illustrated"""

import requests
from bs4 import BeautifulSoup as bs
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt


def url2html(url, _s):
    """Convert url to html"""
    result = _s.get(url)
    return result.text


def html2soup(html):
    """Convert html to a BeautifulSoup object"""
    return bs(html, "html.parser")


def scrape(url, _s):
    """Web scrape url and generate data frame"""
    html = url2html(url, _s)
    soup = html2soup(html)
    # Grab the table with the data
    table = soup.find_all('table')[3]
    # Get the data within the table
    table = table.find_all("td")[0].find_all("tr")[5:]

    data = {}
    county = ""

    for val in table:
        tds = val.find_all('td')
        if len(tds) == 2:
            _c = tds[1].text.strip()
            if not _c == "Utenlands":
                county = _c
                data[county] = [list(range(1, 13)), [-1 for i in range(12)]]
                continue
        if len(tds) < 3:
            continue

        month = int(tds[5].text.strip().split(".")[1])
        data[county][1][month] += 1

    for key in data:
        data[key] = [[it, val] for it, val in enumerate(data[key][1]) if not val == -1]
        data[key] = list(map(list, zip(*data[key])))

    return data

def gen_url(_from, _to):
    """Dynamically generate url"""
    return "https://w2.brreg.no/kunngjoring/kombisok.jsp?" \
           "datoFra=" + _from + "&datoTil=" + _to + "&" \
           "id_region=0&id_niva1=51&id_niva2=-+-+-&id_bransje1=0"

def get_data():
    """Scrape data from url"""

    url_2019 = gen_url("01.03.2019", "31.05.2019")
    url_2020 = gen_url("01.05.2020", "31.05.2020")

    # Initialize requests session
    session = requests.session()

    data2019 = scrape(url_2019, session)
    data2020 = scrape(url_2020, session)

    return [data2019, data2020]

def plot_graph(data2019, data2020):
    """Plot multi-graph"""
    cols = 4
    rows = 3

    fig, axes = plt.subplots(rows, cols)
    for i, (key, val) in enumerate(data2019.items()):
        _ax = axes[int(i / cols)][int(i % cols)]
        _ax.plot(val[0], val[1], c="orange")
        _ax.plot(data2020[key][0], data2020[key][1], c="cyan")
        _ax.set_title(key)

    fig.add_subplot(111, frame_on=False)
    fig.tight_layout()
    plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)

    legend_handles = [Line2D([0], [0], color="orange", lw=2, label="2019"),
                      Line2D([0], [0], color="cyan", lw=2, label="2020")]
    plt.legend(handles=legend_handles, loc="upper left")

    plt.suptitle("Commencement of liquidation proceedings of 2019-2020", fontweight="bold")
    plt.ylabel("Commencement of liquidation proceedings", fontweight="bold")
    plt.xlabel("Months", fontweight="bold")

    plt.savefig("output.pdf")

if __name__ == "__main__":
    plot_graph(*get_data())
