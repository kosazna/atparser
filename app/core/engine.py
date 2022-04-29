# -*- coding: utf-8 -*-

from selenium import webdriver
from typing import Optional, List, Union
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from atparser.app.utils import scroll_down, get_user_agent, state
from time import sleep
from at.logger import log


class SeleniumEngine:
    def __init__(self) -> None:
        self.driver = None
        self.active_element: Optional[WebElement] = None
        self.active_elements: List[WebElement] = []

    def go_to(self, url: str):
        self.driver.get(url)

    def scroll_down(self, rate=1500):
        scroll_down(self.driver, rate)

    def terminate(self):
        self.driver.close()

    def launch(self, browser: str, executable: str):
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

        self.driver.get(self.url)
        sleep(state['launch_delay'])

    def _find_element(self, container, by, element, mode: str = 'single'):
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
                _element = None
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
            else:
                _element = None

        return _element

    def find(self,
             on: Union[str, WebElement],
             by: str,
             element: str,
             set_active: bool = False,
             origin: str = 'single',
             mode: str = 'single',
             store: bool = False):

        if isinstance(on, str):
            if on == 'driver':
                container = self.driver
            elif on == 'active element':
                container = self.active_element
            elif on == 'active elements':
                container = self.active_elements
        else:
            container = on

        if origin == 'multiple':
            if isinstance(container, list):
                _element = [self._find_element(
                    el, by, element, mode) for el in container]
            else:
                raise ValueError(
                    "Origin element must be a list if 'origin=multiple'")
        else:
            if isinstance(container, list):
                raise ValueError(
                    "Origin element must not be a list if 'origin=single'")
            else:
                _element = self._find_element(container, by, element, mode)

        if _element is not None:
            if mode == 'single' and origin == 'single':
                log.success("Element found:\n")
                log.info(_element)

                if set_active:
                    self.active_element = _element   
                    log.success("\nActive element changed.")
                if store:
                    state['single_elements'].append(_element)
                    log.success("Element stored.\n")
            else:
                log.success(f"[{len(_element)}] elements found:\n")
                log.info(_element)
                if set_active:
                    self.active_elements = _element  
                    log.success("\nActive elements changed.") 
                if store:
                    state['multiple_elements'].append(_element)
                    log.success("Elements stored.\n")
        else:
            log.warning(f"Element wasn't found with {by}: {element}")
