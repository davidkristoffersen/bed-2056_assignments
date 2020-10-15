#!/usr/bin/python3
"""Bankcrypties based on covid illustrated"""

import concurrent.futures
from pprint import pprint
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


def scrape(args):
    """Web scrape url and generate data frame"""
    [url, _s] = args
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
                data[county] = 0
                continue
        if len(tds) < 3:
            continue
        data[county] += 1

    return data

def gen_url(_from, _to):
    """Dynamically generate url"""
    return "https://w2.brreg.no/kunngjoring/kombisok.jsp?" \
           "datoFra=" + _from + "&datoTil=" + _to + "&" \
           "id_region=0&id_niva1=51&id_niva2=-+-+-&id_bransje1=0"


def concurrent_scrape(urls, session):
    """Concurrently scrape"""
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url in urls:
            futures.append([url[0], executor.submit(scrape, [url[1], session])])
    return [[f[0], f[1].result()] for f in futures]


def convert_scraped_data(scraped):
    """Convert scraped data"""
    result = {}
    for _m in scraped:
        month = _m[0]
        for key, val in _m[1].items():
            if key not in result:
                result[key] = [[month], [val]]
            else:
                result[key][0].append(month)
                result[key][1].append(val)
    return result


def get_data():
    """Scrape data from url"""

    dates_2019 = [
        ["01.01.2019", "31.01.2019"],
        ["01.02.2019", "28.02.2019"],
        ["01.03.2019", "31.03.2019"],
        ["01.04.2019", "30.04.2019"],
        ["01.05.2019", "31.05.2019"],
        ["01.06.2019", "30.06.2019"],
        ["01.07.2019", "31.07.2019"],
        ["01.08.2019", "31.08.2019"],
        ["01.09.2019", "30.09.2019"],
        ["01.10.2019", "31.10.2019"],
        ["01.11.2019", "30.11.2019"],
        ["01.12.2019", "31.12.2019"]
    ]

    dates_2020 = [
        ["01.01.2020", "31.01.2020"],
        ["01.02.2020", "29.02.2020"],
        ["01.03.2020", "31.03.2020"],
        ["01.04.2020", "30.04.2020"],
        ["01.05.2020", "31.05.2020"],
        ["01.06.2020", "30.06.2020"],
        ["01.07.2020", "31.07.2020"],
        ["01.08.2020", "31.08.2020"],
        ["01.09.2020", "30.09.2020"],
        ["01.10.2020", "15.10.2020"],
    ]

    urls_2019 = [[it + 1, gen_url(*date)] for it, date in enumerate(dates_2019)]
    urls_2020 = [[it + 1, gen_url(*date)] for it, date in enumerate(dates_2020)]

    # Initialize requests session
    session = requests.session()

    data = concurrent_scrape(urls_2019, session)
    data2019 = convert_scraped_data(data)

    data = concurrent_scrape(urls_2020, session)
    data2020 = convert_scraped_data(data)

    pprint(data2019)
    pprint(data2020)

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
