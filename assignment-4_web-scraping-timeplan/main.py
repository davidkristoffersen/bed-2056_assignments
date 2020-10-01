#!/usr/bin/env python3
"""Timeplan web scraping"""

import pandas
import requests
from bs4 import BeautifulSoup


def url2html(url, _s):
    """Convert url to html"""
    result = _s.get(url)
    return result.text


def html2soup(html):
    """Convert html to a BeautifulSoup object"""
    return BeautifulSoup(html, 'html.parser')


def scrape(url, _s):
    """Web scrape url and generate data frame"""
    html = url2html(url, _s)
    soup = html2soup(html)
    # Find div with matching class
    weeks = soup.findAll('div', {'class': 'div_week mb-4'})

    ret = []
    # Append all dates to return list
    for week in weeks:
        _tr = week.find('tr', {'class': 'table-primary'})
        _td = _tr.findNext()
        # Parse out date from _td
        date = _td.renderContents().strip().decode('utf-8').split('<br/>')[1]
        ret.append(date)
    return ret


def gen_data_frame(dates):
    """Generate data frame"""
    data = {'date': dates}
    return pandas.DataFrame(data, columns=['date'])


if __name__ == "__main__":
    URL = "http://timeplan.uit.no/emne_timeplan.php?sem=20h&module%5B%5D=BED-2056-1&View=list"

    # Initialize requests session
    session = requests.session()

    # Web scrape timeplan url
    timeplan_data = scrape(URL, session)

    # Print data frame
    print(gen_data_frame(timeplan_data))
