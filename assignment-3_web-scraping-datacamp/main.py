#!/usr/bin/env python3
"""Test web scraping"""

import requests
from bs4 import BeautifulSoup


def url2soup(url):
    """Convert an url to a beautifulSoup object"""
    return BeautifulSoup(requests.get(url).text, 'html.parser')

PYTHON_URL = "https://learn.datacamp.com/courses/tech:python"
R_URL = "https://learn.datacamp.com/courses/tech:r"

python_soup = url2soup(PYTHON_URL)
r_soup = url2soup(R_URL)

print(python_soup.find_all('h2'))
print(r_soup.find_all('h2'))
