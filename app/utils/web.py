# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

ua = UserAgent()


def get_headers(browser: str = 'firefox') -> dict:
    if browser == 'firefox':
        _headers = {
            "User-Agent": f"{ua.firefox}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    else:
        _headers = {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": f"{ua.chrome}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }

    return _headers


def get_user_agent(browser: str = 'firefox') -> str:
    return ua.firefox if browser == 'firefox' else ua.chrome


def request_soup(url: str, browser: str = 'firefox') -> BeautifulSoup:
    headers = get_headers(browser)

    _r = requests.get(url, headers=headers)
    _soup = BeautifulSoup(_r.text, 'lxml')

    return _soup
