#!/usr/bin/env python3
"""Test web scraping"""

import csv
import requests
from bs4 import BeautifulSoup


def login(url, username, password, _s):
    """Login to session"""
    _s.get(url)
    login_data = {'user[email]': username, 'user[password]': password}
    _s.post(url, data=login_data)


def url2html(url, _s):
    """Convert url to html"""
    result = _s.get(url)
    return result.text


def html2soup(html):
    """Convert html to a beautifulSoup object"""
    return BeautifulSoup(html, 'html.parser')


def scrape(url, _s):
    """Web scrape url and generate data frame"""
    html = url2html(url, _s)
    soup = html2soup(html)
    main = soup.find('div', {'class': 'courses__explore-list js-async-bookmarking row'})

    ret = []
    for child in main.findChildren(recursive=False):
        ret.append(child.find('h4').string)
    return ret


def gen_data_frame(language, tech):
    """Generate required data frame"""
    return {'language': language, 'tech': tech}


def get_user_credentials(use_csv):
    """Get user credentials from csv file"""
    if use_csv:
        with open('user-credentials.csv', 'r') as file:
            creds = next(csv.reader(file))
            return {'username': creds[0], 'password': creds[1]}

    print("Username: ", end="")
    username = input()
    print("Password: ", end="")
    password = input()
    return {'username': username, 'password': password}

if __name__ == "__main__":
    LOGIN_URL = "https://www.datacamp.com/users/sign_in"
    PYTHON_URL = "https://www.datacamp.com/courses/tech:python?embedded=true"
    R_URL = "https://www.datacamp.com/courses/tech:r?embedded=true"
    USE_CSV = True

    credentials = get_user_credentials(USE_CSV)
    session = requests.session()
    login(LOGIN_URL, credentials['username'], credentials['password'], session)

    python_tech = scrape(PYTHON_URL, session)
    r_tech = scrape(R_URL, session)

    print(gen_data_frame('python', python_tech))
    print(gen_data_frame('r', r_tech))
