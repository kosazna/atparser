# -*- coding: utf-8 -*-

from time import sleep
from selenium.webdriver.remote.webelement import WebElement
from typing import TypeVar

SeleniumWebdriver = TypeVar("SeleniumWebdriver")


def one_time_scroll(driver: SeleniumWebdriver, scrollby: int = 1500):
    driver.execute_script(f"window.scrollTo(0, {scrollby});")


def scroll_down(driver: SeleniumWebdriver, scrollby: int = 1500, wait: float = 0.2):
    max_y = driver.execute_script("return document.body.scrollHeight")
    go_y = scrollby
    while go_y < max_y:
        driver.execute_script(f"window.scrollTo(0, {go_y});")
        go_y += scrollby
        sleep(wait)


def get_element_attributes(driver: SeleniumWebdriver, element: WebElement) -> dict:
    script = """
    var items = {};
    for (index = 0; index < arguments[0].attributes.length; ++index) {
    items[arguments[0].attributes[index].name] =
        arguments[0].attributes[index].value;
    }
    var elemText = arguments[0].textContent.trim();

    if (elemText != "") {
    items.text = elemText;
    }

    return items;
    """

    _attrs = driver.execute_script(script, element)

    return _attrs
