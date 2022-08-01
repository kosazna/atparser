# -*- coding: utf-8 -*-
import sys
from typing import Any, Optional, Tuple

from at.auth.client import AuthStatus
from at.gui import *
from at.logger import log
from at.result import Result
from atparser.app.settings import *
from atparser.app.utils import paths, state
from at.web import Element
from atparser.app.core import SeleniumEngine, BeautifulSoupEngine
from PyQt5.QtCore import Qt, QThreadPool, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

# When setting fixed width to QLineEdit ->
# -> add alignment=Qt.AlignLeft when adding widget to layout


class ParserTab(AtWidget):
    def __init__(self,
                 size: Tuple[Optional[int]] = (None, None),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.seleniumEngine = SeleniumEngine()
        self.bsEngine = BeautifulSoupEngine()
        self.initUi(size)

    def setupUi(self, size):
        set_size(widget=self, size=size)

        # layout = QHBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(2, 4, 2, 0)

        urlLayout = QVBoxLayout()
        topButtonLayout = QHBoxLayout()
        seleniumParamsLayout = QHBoxLayout()
        bs4ParamsLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        historyLayout = QHBoxLayout()
        actionElemLayout = QVBoxLayout()
        attrsLayout = QHBoxLayout()
        parseFromLayout = QHBoxLayout()

        self.url = StrInput(label='URL',
                            parent=self)

        self.buttonRequest = Button(label='Request',
                                    size=(100, 24),
                                    parent=self)

        self.buttonLaunch = Button(label='Launch',
                                   size=(100, 24),
                                   parent=self)

        self.buttonRefresh = Button(label='Refresh',
                                    size=(100, 24),
                                    parent=self)

        self.buttonGetCookies = Button(label='Get Cookies',
                                       size=(100, 24),
                                       parent=self)

        self.buttonScroll = Button(label='Scroll down',
                                   size=(100, 24),
                                   parent=self)

        self.parseFromCombo = ComboInput(label='Parse from',
                                         items=('Driver',
                                                'Soup',
                                                'Active element',
                                                'History'),
                                         combosize=(120, 24),
                                         parent=self)
        self.parseFromStatus = StatusLabel(statussize=(650, 22),
                                           parent=self)

        self.history = ComboInput(label='History',
                                  combosize=(500, 24),
                                  parent=self)

        self.buttonSetActiveFromHistory = Button(label='Set active',
                                                 size=(100, 24),
                                                 parent=self)

        self.targetCombo = ComboInput(label='Target',
                                      items=('single', 'multiple'),
                                      parent=self)

        self.engineSelect = ComboInput(label='Engine',
                                       items=('Selenium', 'BS4'),
                                       parent=self)

        self.findParams = ComboInput(label='Params',
                                     items=FIND_PARAMS,
                                     combosize=(120, 24),
                                     parent=self)

        self.elementParams = StrInput(parent=self)

        self.tagElem = ComboInput(label='Tag',
                                  items=MOST_COMMON_HTML_TAGS,
                                  combosize=(120, 24),
                                  parent=self)

        self.classParam = StrInput(label='Class',
                                   parent=self)

        self.cssParam = StrInput(label='Css',
                                 parent=self)

        self.idParam = StrInput(label='Id',
                                parent=self)

        self.attrsCombo = ComboInput(label='Attrs',
                                     combosize=(200, 24),
                                     parent=self)

        self.buttonGetAttribute = Button(label='Get attribute',
                                         size=(150, 24),
                                         parent=self)

        self.buttonFind = Button(label='Find Element',
                                 color='blue',
                                 size=(200, 30),
                                 parent=self)
        self.buttonSetActive = Button(label='Set active',
                                      size=(150, 24),
                                      parent=self)
        self.buttonStore = Button(label='Add to history',
                                        size=(150, 24),
                                        parent=self)

        self.buttonClick = Button(label='Click',
                                        size=(150, 24),
                                        parent=self)

        self.status = StatusButton(parent=self)

        self.statusSelenium = StatusLabel('SE driver',
                                          statussize=(160, 22),
                                          parent=self)
        self.statusBS = StatusLabel('BSE Soup',
                                    statussize=(160, 22),
                                    parent=self)

        urlLayout.addWidget(self.url)
        topButtonLayout.addWidget(self.buttonRequest)
        topButtonLayout.addWidget(self.buttonLaunch, alignment=Qt.AlignRight)
        topButtonLayout.addWidget(self.buttonRefresh)
        topButtonLayout.addWidget(self.buttonScroll)
        topButtonLayout.addWidget(self.buttonGetCookies)
        urlLayout.addLayout(topButtonLayout)
        mainLayout.addLayout(urlLayout)
        mainLayout.addWidget(HLine())
        mainLayout.addWidget(self.parseFromStatus, alignment=Qt.AlignHCenter)
        parseFromLayout.addWidget(self.parseFromCombo)
        parseFromLayout.addWidget(self.statusSelenium)
        parseFromLayout.addWidget(self.statusBS)
        mainLayout.addLayout(parseFromLayout)
        historyLayout.addWidget(self.history)
        historyLayout.addWidget(self.buttonSetActiveFromHistory)
        mainLayout.addLayout(historyLayout)
        mainLayout.addWidget(self.targetCombo)
        mainLayout.addWidget(self.engineSelect)
        mainLayout.addWidget(HLine())
        seleniumParamsLayout.addWidget(self.findParams)
        seleniumParamsLayout.addWidget(self.elementParams, stretch=2)
        mainLayout.addLayout(seleniumParamsLayout)
        mainLayout.addWidget(HLine())
        bs4ParamsLayout.addWidget(self.tagElem)
        bs4ParamsLayout.addWidget(self.classParam)
        bs4ParamsLayout.addWidget(self.idParam)
        bs4ParamsLayout.addWidget(self.cssParam)
        mainLayout.addLayout(bs4ParamsLayout)
        mainLayout.addWidget(HLine())
        attrsLayout.addWidget(self.attrsCombo)
        attrsLayout.addWidget(self.buttonGetAttribute, alignment=Qt.AlignRight)
        attrsLayout.addWidget(self.buttonClick)
        mainLayout.addLayout(attrsLayout)
        mainLayout.addWidget(HLine())
        actionElemLayout.addWidget(self.buttonSetActive)
        actionElemLayout.addWidget(self.buttonStore)
        buttonLayout.addWidget(self.buttonFind, alignment=Qt.AlignCenter)
        buttonLayout.addLayout(actionElemLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.status, stretch=2, alignment=Qt.AlignBottom)

        # sideLayout.addWidget(self.statusSelenium)
        # sideLayout.addWidget(self.statusBS, alignment=Qt.AlignTop, stretch=2)

        # layout.addLayout(mainLayout)
        # layout.addLayout(sideLayout)

        self.setLayout(mainLayout)

    def initUi(self, size: tuple):
        self.setupUi(size)
        self.popup.set_appname(state['appname'])
        self.parseFromCombo.setCurrentText('Driver')
        self.statusSelenium.changeStatus('offline', 'statusError')
        self.statusBS.changeStatus('no data', 'statusError')
        self.parseFromCombo.subscribe(self.onParseFromChange)
        self.buttonLaunch.subscribe(self.onLaunch)
        self.buttonFind.subscribe(self.onFindElement)
        self.buttonSetActive.subscribe(self.onSetActiveElement)
        self.buttonStore.subscribe(self.onStoreElement)
        self.buttonSetActiveFromHistory.subscribe(self.onSetActiveFromHistory)
        self.buttonGetAttribute.subscribe(self.onGetElementAttribute)
        self.buttonClick.subscribe(self.onClick)
        self.buttonGetCookies.subscribe(self.onGetCookies)
        self.buttonRefresh.subscribe(self.onRefresh)
        self.buttonScroll.subscribe(self.onScrollDown)
        self.buttonRequest.subscribe(lambda: self.runThread(self.onRequest))

    def getParams(self, key: Optional[str] = None):
        params = {
            'engine': self.engineSelect.getCurrentText(),
            'url': self.url.getText(),
            'parse_from': self.parseFromCombo.getCurrentText(),
            'history': self.history.getCurrentText(),
            'target': self.targetCombo.getCurrentText(),
            'selenium_find_by': self.findParams.getCurrentText(),
            'selenium_find_params': self.elementParams.getText(),
            'bs_tag': self.tagElem.getCurrentText(),
            'bs_class': self.classParam.getText(),
            'bs_id': self.idParam.getText(),
            'bs_css': self.cssParam.getText(),
            'attribute': self.attrsCombo.getCurrentText()
        }

        return params if key is None else params.get(key)

    def selectEngine(self):
        _engine = self.engineSelect.getCurrentText()

        if _engine == "Selenium":
            return self.seleniumEngine
        else:
            return self.bsEngine

    def onGetCookies(self):
        if self.seleniumEngine.driver is not None:
            cookies = self.seleniumEngine.get_cookies()
            log.info(cookies)
        else:
            log.error("Driver is not launched. Can't get cookies")

    def onScrollDown(self):
        if self.seleniumEngine.driver is not None:
            self.seleniumEngine.scroll_down()
        else:
            log.error("Driver is not launched. Can't scroll down")

    def onRefresh(self):
        if self.seleniumEngine.driver is not None:
            self.seleniumEngine.refresh()
        else:
            log.error("Driver is not launched. Can't refresh page")

    @needs(('url'))
    def onRequest(self, _progress):
        url = self.getParams('url')
        self.bsEngine = BeautifulSoupEngine.from_request(url)

        self.parseFromCombo.setCurrentText('Soup')
        self.statusBS.changeStatus('data available', 'statusOk')

    def click(self, _progress):
        if self.seleniumEngine.driver is not None and self.seleniumEngine.active_element is not None:
            self.seleniumEngine.click()
        else:
            log.error("No active element to click.")

    def onClick(self):
        run_thread(threadpool=self.threadpool,
                   function=self.click,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def onLaunch(self):
        _webdriver = state['webdriver']
        _url = self.getParams('url')

        if _webdriver == 'Firefox':
            _webdriver_exe = paths.get_firefoxdriver()
        else:
            _webdriver_exe = paths.get_chromedriver()

        self.seleniumEngine.launch(_webdriver, _webdriver_exe, _url)
        self.statusSelenium.changeStatus('online', 'statusOk')

    def onParseFromChange(self):
        combo_text = self.parseFromCombo.getCurrentText()

        if combo_text == 'Driver':
            self.parseFromStatus.setText('Selenium WebDriver')
            self.history.clearItems()
            self.engineSelect.setCurrentText("Selenium")
        if combo_text == 'Soup':
            self.parseFromStatus.setText('BeautifulSoup')
            self.history.clearItems()
            self.engineSelect.setCurrentText("BS4")
        elif combo_text == 'Active element':
            _engine = self.selectEngine()
            self.parseFromStatus.setText(_engine.active_element_name)
            self.history.clearItems()
        else:
            self.parseFromStatus.setText('History')
            self.history.clearItems()
            self.history.addItems(state['history'].keys())

    def findElement(self, _progress):
        params = self.getParams()
        parse_from = params['parse_from']

        if parse_from == 'History':
            _element = params['history']
            origin = state['history'][_element]
        else:
            origin = parse_from

        _engine = self.engineSelect.getCurrentText()
        target = params['target']

        if _engine == 'Selenium':
            by = params['selenium_find_by']
            element = params['selenium_find_params']

            element = Element.from_text(f"{by}={element}")

            self.seleniumEngine.find(origin=origin,
                                     element=element,
                                     target=target)
        else:
            tagParam = params['bs_tag']
            classParam = params['bs_class'] or None
            idParam = params['bs_id'] or None
            cssParam = params['bs_css'] or None

            element = Element(tag_name=tagParam,
                              class_name=classParam,
                              id=idParam,
                              css_selector=cssParam)

            if self.seleniumEngine.is_online:
                self.bsEngine.refresh_soup_from_selenium_engine(
                    self.seleniumEngine)

            self.bsEngine.find(origin=origin,
                               element=element,
                               target=target)

    def onFindElement(self):
        run_thread(threadpool=self.threadpool,
                   function=self.findElement,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def getElementAttribute(self, _progress):
        _attr = self.getParams('attribute')

        _engine = self.selectEngine()

        texts = _engine.get_attribute(_attr)

        if isinstance(texts, list):
            for idx, _text in enumerate(texts):
                log.info(f"{idx} - {_text}")
        else:
            log.info(texts)

    def onGetElementAttribute(self):
        run_thread(threadpool=self.threadpool,
                   function=self.getElementAttribute,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def setActiveElement(self, _progress):
        _engine = self.selectEngine()
        _engine.set_active()
        self.attrsCombo.clearItems()
        self.attrsCombo.addItems(_engine.active_element_attrs)
        self.parseFromCombo.setCurrentText('Active element')

        self.onParseFromChange()

    def onSetActiveElement(self):
        run_thread(threadpool=self.threadpool,
                   function=self.setActiveElement,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def storeElement(self, _progress):
        _engine = self.selectEngine()
        _engine.store_element()

        _parseFrom = self.getParams('parse_from')

        if _parseFrom == "History":
            _activeHistoryElement = self.history.getCurrentText()
            self.history.clearItems()
            self.history.addItems(state['history'])
            self.history.setCurrentText(_activeHistoryElement)

    def onStoreElement(self):
        run_thread(threadpool=self.threadpool,
                   function=self.storeElement,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def setActiveFromHistory(self, _progress):
        history_element_name = self.getParams('history')

        if history_element_name:
            _engine = self.selectEngine()

            _engine.set_active_from_history(history_element_name)
            self.parseFromCombo.setCurrentText('Active element')
        else:
            log.warning("No element was chosen from history")

    def onSetActiveFromHistory(self):
        run_thread(threadpool=self.threadpool,
                   function=self.setActiveFromHistory,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)


if __name__ == '__main__':
    cssGuide = paths.get_css(obj=True).joinpath("_style.css").read_text()
    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = ParserTab(size=(600, None))
    ui.setStyleSheet(cssGuide)
    ui.show()

    sys.exit(app.exec_())
