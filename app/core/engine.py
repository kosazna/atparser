# -*- coding: utf-8 -*-

from selenium import webdriver
from typing import Optional, List, Union, Dict
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from atparser.app.utils import (scroll_down,
                                get_user_agent,
                                state,
                                get_element_attributes,
                                Element)
from time import sleep
from at.logger import log


class SeleniumEngine:
    def __init__(self) -> None:
        self.driver = None
        self.active_element_name: str = ''
        self.active_element_attrs: Optional[list] = None
        self.active_element: Optional[Union[WebElement,
                                            List[WebElement]]] = None
        self.found_element_name: str = ''
        self.found_element: Optional[Union[WebElement,
                                           List[WebElement]]] = None

    def go_to(self, url: str):
        self.driver.get(url)

    def scroll_down(self, rate=1500):
        scroll_down(self.driver, rate)

    def terminate(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()
    
    def get_cookies(self):
        return self.driver.get_cookies()

    def click(self):
        self.active_element.click()

    def launch(self, browser: str, executable: str, url: str):
        if browser == 'Chrome':
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument(
                f"user-agent={get_user_agent('chrome')}")
            self.driver = webdriver.Chrome(executable, options=chrome_options)
        elif browser == 'Firefox':
            profile = webdriver.FirefoxProfile()
            agent = get_user_agent('firefox')
            profile.set_preference(
                "general.useragent.override", agent)
            self.driver = webdriver.Firefox(firefox_profile=profile,
                                            executable_path=executable)
            self.driver.maximize_window()
        else:
            print(f'Browser not supported: {browser}')
            return

        self.driver.get(url)

    def _find_element(self, container, element: Element, mode: str = 'single'):
        try:
            if mode == 'multiple':
                _element = container.find_elements(**element.selenium_props())
            else:
                _element = container.find_element(**element.selenium_props())

            return _element
        except NoSuchElementException:
            log.error(f"NoSuchElementException -> {element}")
            return None
        except StaleElementReferenceException:
            log.error(f"StaleElementReferenceException -> {element}")
            return None

    def find(self,
             origin: Union[str, WebElement],
             element: str,
             target: str = 'single'):

        if isinstance(origin, str):
            if origin == 'Driver':
                container = self.driver
            else:
                container = self.active_element
        else:
            container = origin

        if isinstance(container, list):
            _element = [self._find_element(el, element, target)
                        for el in container]
        else:
            _element = self._find_element(container, element, target)

        if _element is not None:
            if isinstance(_element, list):
                if any(_element):
                    _elems = [_el for _el in _element if _el is not None]
                    name_tag = f"{len(_elems)} | Selenium | {element}"
                    log.success(
                        f"\n[{len(_elems)}] elements found | Name Tag: [{name_tag}]")
                    for idx, el in enumerate(_elems):
                        log.highlight(f"\n{idx}")
                        _attrs = self.get_element_attributes(el)
                        for _attr in _attrs:
                            log.info(f"{_attr}: {_attrs[_attr]}")
                    self.found_element_name = name_tag
                    self.found_element = _elems
                else:
                    log.warning(f"{element} wasn't found")
            else:
                name_tag = f"Single | Selenium | {element}"
                log.success(f"\nElement found | Name Tag: [{name_tag}]")
                _attrs = self.get_element_attributes(_element)
                for _attr in _attrs:
                    log.info(f"{_attr}: {_attrs[_attr]}")
                self.found_element_name = name_tag
                self.found_element = _element
        else:
            log.warning(f"{element} wasn't found")

    def set_active(self,
                   element_name: Optional[str] = None,
                   element: Optional[WebElement] = None):
        if element_name is None:
            self.active_element = self.found_element
            self.active_element_name = self.found_element_name
        else:
            self.active_element = element
            self.active_element_name = element_name
        self.active_element_attrs = list(self.get_element_attributes().keys())
        log.success(
            f"\nActive element changed to [{self.active_element_name}].\n")

    def set_active_from_history(self, element: str):
        _el_name = element
        _el = state['history'][_el_name]
        self.set_active(_el_name, _el)

    def store_element(self):
        state['history'].update({self.found_element_name: self.found_element})
        log.success(f"\nElement [{self.found_element_name}] stored.\n")

    def get_element_attributes(self, element: Optional[WebElement] = None):
        if element is None:
            if isinstance(self.active_element, list):
                _attrs = get_element_attributes(
                    self.driver, self.active_element[0])
            else:
                _attrs = get_element_attributes(
                    self.driver, self.active_element)
        else:
            if isinstance(element, list):
                _attrs = get_element_attributes(self.driver, element[0])
            else:
                _attrs = get_element_attributes(self.driver, element)

        return _attrs

    def get_attribute(self, attribute: str):
        if attribute == 'text':
            _attribute = 'textContent'
        else:
            _attribute = attribute

        if isinstance(self.active_element, list):
            return [ae.get_attribute(_attribute) for ae in self.active_element]
        else:
            return self.active_element.get_attribute(_attribute)


class BeautifulSoupEngine:
    def __init__(self) -> None:
        self.soup = None
        self.active_element_name: str = ''
        self.active_element_attrs: Optional[list] = None
        self.active_element: Optional[Union[WebElement,
                                            List[WebElement]]] = None
        self.found_element_name: str = ''
        self.found_element: Optional[Union[WebElement,
                                           List[WebElement]]] = None

    def _find_element(self, container, element: Element, mode: str = 'single'):
        try:
            if mode == 'multiple':
                _element = container.find_elements(**element.selenium_props())
            else:
                _element = container.find_element(**element.selenium_props())

            return _element
        except NoSuchElementException:
            log.error(f"NoSuchElementException -> {element}")
            return None
        except StaleElementReferenceException:
            log.error(f"StaleElementReferenceException -> {element}")
            return None

    def find(self,
             origin: Union[str, WebElement],
             element: str,
             target: str = 'single'):

        if isinstance(origin, str):
            if origin == 'Driver':
                container = self.driver
            else:
                container = self.active_element
        else:
            container = origin

        if isinstance(container, list):
            _element = [self._find_element(el, element, target)
                        for el in container]
        else:
            _element = self._find_element(container, element, target)

        if _element is not None:
            if isinstance(_element, list):
                if any(_element):
                    _elems = [_el for _el in _element if _el is not None]
                    name_tag = f"{len(_elems)} | Selenium | {element}"
                    log.success(
                        f"\n[{len(_elems)}] elements found | Name Tag: [{name_tag}]")
                    for idx, el in enumerate(_elems):
                        log.highlight(f"\n{idx}")
                        _attrs = self.get_element_attributes(el)
                        for _attr in _attrs:
                            log.info(f"{_attr}: {_attrs[_attr]}")
                    self.found_element_name = name_tag
                    self.found_element = _elems
                else:
                    log.warning(f"{element} wasn't found")
            else:
                name_tag = f"Single | Selenium | {element}"
                log.success(f"\nElement found | Name Tag: [{name_tag}]")
                _attrs = self.get_element_attributes(_element)
                for _attr in _attrs:
                    log.info(f"{_attr}: {_attrs[_attr]}")
                self.found_element_name = name_tag
                self.found_element = _element
        else:
            log.warning(f"{element} wasn't found")

    def set_active(self,
                   element_name: Optional[str] = None,
                   element: Optional[WebElement] = None):
        if element_name is None:
            self.active_element = self.found_element
            self.active_element_name = self.found_element_name
        else:
            self.active_element = element
            self.active_element_name = element_name
        self.active_element_attrs = list(self.get_element_attributes().keys())
        log.success(
            f"\nActive element changed to [{self.active_element_name}].\n")

    def set_active_from_history(self, element: str):
        _el_name = element
        _el = state['history'][_el_name]
        self.set_active(_el_name, _el)

    def store_element(self):
        state['history'].update({self.found_element_name: self.found_element})
        log.success(f"\nElement [{self.found_element_name}] stored.\n")

    def get_element_attributes(self, element: Optional[WebElement] = None):
        if element is None:
            if isinstance(self.active_element, list):
                _attrs = get_element_attributes(
                    self.driver, self.active_element[0])
            else:
                _attrs = get_element_attributes(
                    self.driver, self.active_element)
        else:
            if isinstance(element, list):
                _attrs = get_element_attributes(self.driver, element[0])
            else:
                _attrs = get_element_attributes(self.driver, element)

        return _attrs

    def get_attribute(self, attribute: str):
        if attribute == 'text':
            _attribute = 'textContent'
        else:
            _attribute = attribute

        if isinstance(self.active_element, list):
            return [ae.get_attribute(_attribute) for ae in self.active_element]
        else:
            return self.active_element.get_attribute(_attribute)
