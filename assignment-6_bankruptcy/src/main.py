#!/usr/bin/python3
"""Bankcrypties based on covid illustrated"""

import re
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


def is_county(elem):
    """Check if county"""
    tds = elem.find_all('td')
    if len(tds) == 2:
        return True, tds[1].text.strip()

    return False, ""


def get_date(elem):
    """Get date"""
    tds = elem.find_all('td')
    if len(tds) < 3:
        return False, ""
    date = tds[5].text.strip()

    days = {3: 31, 4: 30 + 31, 5: 31 + 31 + 30}
    day = int(date.split(".")[0])
    month = int(date.split(".")[1])

    index = days[month] + day
    return True, index


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
        is_count, count = is_county(val)
        if is_count:
            county = count
            data[county] = {}
            continue

        is_firm, index = get_date(val)
        if not is_firm:
            continue

        if  index  not in data[county]:
            data[county][index] = 0

        data[county][index] += 1

    if "Utenlands" in data:
        del data["Utenlands"]
    if "Svalbard" in data:
        del data["Svalbard"]

    return data

def gen_url(_from, _to):
    """Dynamically generate url"""
    return "https://w2.brreg.no/kunngjoring/kombisok.jsp?" \
           "datoFra=" + _from + "&datoTil=" + _to + "&" \
           "id_region=0&id_niva1=51&id_niva2=-+-+-&id_bransje1=0"

def get_data():
    """Scrape data from url"""

    url_2019 = gen_url("01.05.2019", "31.05.2019")
    url_2020 = gen_url("01.05.2020", "31.05.2020")

    # Initialize requests session
    session = requests.session()

    data2019 = scrape(url_2019, session)
    data2020 = scrape(url_2020, session)

    return [data2019, data2020]

    # example_x = list(range(10))
    # example_y = list(range(0, 20, 2))
    # example_y2 = list(range(0, 30, 3))
    # example_y3 = list(range(0, 40, 4))
    # example_y4 = list(range(0, 50, 5))

    # example_data_2019 = {
        # "Oslo": [example_x, example_y],
        # "Rogaland": [example_x, example_y2],
        # "Møre og Romsdal": [example_x, example_y3],
        # "Nordland": [example_x, example_y4],
    # }
    # example_data_2020 = {
        # "Oslo": [example_x, example_y4],
        # "Rogaland": [example_x, example_y3],
        # "Møre og Romsdal": [example_x, example_y2],
        # "Nordland": [example_x, example_y],
    # }

    # return [example_data_2019, example_data_2020]

def plot_graph(data2019, data2020):
    """Plot multi-graph"""
    cols = 2
    rows = 2
    print(data2019)
    # print(data2020)
    return

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

    plt.suptitle("Commencement of liquidation proceedings of 2020", fontweight="bold")
    plt.ylabel("Commencement of liquidation proceedings", fontweight="bold")
    plt.xlabel("Days sinces July", fontweight="bold")

    plt.savefig("output.pdf")

if __name__ == "__main__":
    plot_graph(*get_data())
