#!/usr/bin/env python3
"""Timeplan web scraping"""

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
    main = soup.find('div', {'class': 'courses__explore-list js-async-bookmarking row'})

    ret = []
    # Append all tech names to return list
    for child in main.findChildren(recursive=False):
        ret.append(child.find('h4').string)
    return ret


def gen_data_frame(data):
    """Generate data frame"""
    return {'data': data}


if __name__ == "__main__":
    URL = "http://timeplan.uit.no/emne_timeplan.php?sem=20h&module%5B%5D=BED-2056-1&View=list"

    # Initialize requests session
    session = requests.session()

    # Web scrape timeplan url
    timeplan_data = scrape(URL, session)

    # Print data frame
    print(gen_data_frame(timeplan_data))
