# -*- coding: utf-8 -*-

from selenium import webdriver
from typing import Optional, List, Union, Dict
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from atparser.app.utils import (scroll_down,
                                get_user_agent,
                                state,
                                get_element_attributes)
from time import sleep
from at.logger import log


class SeleniumEngine:
    def __init__(self) -> None:
        self.driver = None
        self.active_element_name: str = ''
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
        sleep(state['launch_delay'])

    def _find_element(self, container, by, element, mode: str = 'single'):
        try:
            if mode == 'multiple':
                if by == 'class':
                    _element = container.find_elements(By.CLASS_NAME, element)
                elif by == 'id':
                    _element = container.find_elements(By.ID, element)
                elif by == 'xpath':
                    _element = container.find_elements(By.XPATH, element)
                elif by == 'css':
                    _element = container.find_elements(By.CSS_SELECTOR, element)
                elif by == 'tag':
                    _element = container.find_elements(By.TAG_NAME, element)
            else:
                if by == 'class':
                    _element = container.find_element(By.CLASS_NAME, element)
                elif by == 'id':
                    _element = container.find_element(By.ID, element)
                elif by == 'xpath':
                    _element = container.find_element(By.XPATH, element)
                elif by == 'css':
                    _element = container.find_element(By.CSS_SELECTOR, element)
                elif by == 'tag':
                    _element = container.find_element(By.TAG_NAME, element)

            return _element
        except NoSuchElementException as e:
            log.error(e)
            return None

    def find(self,
             origin: Union[str, WebElement],
             by: str,
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
            _element = [self._find_element(
                el, by, element, target) for el in container]
        else:
            _element = self._find_element(container, by, element, target)

        if _element is not None:
            if isinstance(_element, list):
                name_tag = f"{len(_element)} | {by} | {element}"
                log.success(f"\n[{len(_element)}] elements found | Name Tag: [{name_tag}]")
                for idx, el in enumerate(_element):
                    log.info(f"{idx} - {repr(el)}\n")
                
            else:
                name_tag = f"Single | {by} | {element}"
                log.success(f"\nElement found | Name Tag: [{name_tag}]")
                # log.info(self.get_element_attributes(_element))
                _attrs = self.get_element_attributes(_element)
                for _attr in _attrs:
                    log.info(f"{_attr}: {_attrs[_attr]}")
                name_tag = f"Single | {by} | {element}"
            self.found_element_name = name_tag
            self.found_element = _element
        else:
            log.warning(f"\nElement wasn't found with {by}: {element}")

    def set_active(self):
        self.active_element = self.found_element
        self.active_element_name = self.found_element_name
        log.success("\nActive element changed.\n")

    def set_active_from_history(self, element: str):
        self.active_element = state['history'][element]
        self.active_element_name = element
        log.success("\nActive element changed from history.\n")

    def store_element(self):
        state['history'].update({self.found_element_name: self.found_element})
        log.success("\nElement stored.\n")

    def get_element_attributes(self, element:Optional[WebElement] = None):
        if element is None:
            _attrs = get_element_attributes(self.driver, self.active_element)
        else:
            _attrs = get_element_attributes(self.driver, element)

        return _attrs
