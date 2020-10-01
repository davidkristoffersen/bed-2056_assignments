#!/usr/bin/env python3
"""Test web scraping"""

import requests
from bs4 import BeautifulSoup


def url2soup(url):
    """Convert an url to a beautifulSoup object"""
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def get_data(url):
    """Web scrape url and generate data frame"""
    soup = url2soup(url)
    body_div = soup.html.body.div
    # print(dir(body_div))
    div_div = body_div.find('div', {"class": "dc-account-modal__wrapper js-modal js-account-modal"}, recursive=False)
    print(div_div)
    # section = div_div.find('section', {'class': 'courses__explore '}, recursive=False)
    # print(section)
    # print(body_div.find("section", {"class": "courses__explore"}))
    # div_div = soup.find('div', {'id': '__next'})
    # print(soup.findAll("div", {"class": "courses__explore-list"}))
    # return None

if __name__ == "__main__":
    # PYTHON_URL = "https://www.datacamp.com/courses/tech:python?embedded=true"
    # R_URL = "https://www.datacamp.com/courses/tech:r?embedded=true"
    PYTHON_URL = "https://learn.datacamp.com/courses/tech:python"
    R_URL = "https://learn.datacamp.com/courses/tech:r"

    get_data(PYTHON_URL)
    # print(python_data)

    # r_data = get_data(R_URL)
    # print(r_data)
