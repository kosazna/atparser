# -*- coding: utf-8 -*-
import sys
from typing import Any, Optional, Tuple

from at.auth.client import AuthStatus
from at.gui.components import *
from at.gui.utils import set_size
from at.gui.worker import run_thread
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


class ParserTab(QWidget):
    def __init__(self,
                 size: Tuple[Optional[int]] = (None, None),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.seleniumEngine = SeleniumEngine()
        self.bsEngine = BeautifulSoupEngine()
        self.setupUi(size)
        self.threadpool = QThreadPool(parent=self)
        self.popup = Popup(state['appname'])

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

    def setupUi(self, size):
        set_size(widget=self, size=size)

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 4, 2, 0)

        urlLayout = QVBoxLayout()
        topButtonLayout = QHBoxLayout()
        engineChecksLayout = QVBoxLayout()
        seleniumParamsLayout = QHBoxLayout()
        bs4ParamsLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        historyLayout = QHBoxLayout()
        parseFromLayout = QHBoxLayout()
        actionElemLayout = QVBoxLayout()
        attrsLayout = QHBoxLayout()

        self.url = StrInput(label='URL',
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
        self.parseFromStatus = StatusLabel(statussize=(400, 22),
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

        self.parseFromStatus.setText('Selenium WebDriver')
        self.url.setText(
            "https://www.skroutz.gr/c/40/kinhta-thlefwna.html?from=families")

        urlLayout.addWidget(self.url)
        topButtonLayout.addWidget(self.buttonLaunch, alignment=Qt.AlignRight)
        topButtonLayout.addWidget(self.buttonRefresh)
        topButtonLayout.addWidget(self.buttonScroll)
        topButtonLayout.addWidget(self.buttonGetCookies)
        urlLayout.addLayout(topButtonLayout)
        layout.addLayout(urlLayout)
        layout.addWidget(HLine())
        parseFromLayout.addWidget(self.parseFromCombo)
        parseFromLayout.addWidget(self.parseFromStatus, stretch=2)
        engineChecksLayout.addLayout(parseFromLayout)
        layout.addLayout(engineChecksLayout)
        historyLayout.addWidget(self.history)
        historyLayout.addWidget(self.buttonSetActiveFromHistory)
        layout.addLayout(historyLayout)
        layout.addWidget(self.targetCombo)
        layout.addWidget(self.engineSelect)
        layout.addWidget(HLine())
        seleniumParamsLayout.addWidget(self.findParams)
        seleniumParamsLayout.addWidget(self.elementParams, stretch=2)
        layout.addLayout(seleniumParamsLayout)
        layout.addWidget(HLine())
        bs4ParamsLayout.addWidget(self.tagElem)
        bs4ParamsLayout.addWidget(self.classParam)
        bs4ParamsLayout.addWidget(self.idParam)
        layout.addLayout(bs4ParamsLayout)
        layout.addWidget(HLine())
        attrsLayout.addWidget(self.attrsCombo)
        attrsLayout.addWidget(self.buttonGetAttribute, alignment=Qt.AlignRight)
        attrsLayout.addWidget(self.buttonClick)
        layout.addLayout(attrsLayout)
        layout.addWidget(HLine())
        actionElemLayout.addWidget(self.buttonSetActive)
        actionElemLayout.addWidget(self.buttonStore)
        buttonLayout.addWidget(self.buttonFind, alignment=Qt.AlignCenter)
        buttonLayout.addLayout(actionElemLayout)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.status, stretch=2, alignment=Qt.AlignBottom)
        self.setLayout(layout)

    def updateProgress(self, metadata: dict):
        if metadata:
            progress_now = metadata.get('pbar', None)
            progress_max = metadata.get('pbar_max', None)
            status = metadata.get('status', None)
            count = metadata.get('count', None)

            if progress_now is not None:
                self.progress.setValue(progress_now)
            if progress_max is not None:
                self.progress.setMaximum(progress_max)
            if status is not None:
                self.status.disable(str(status))
            if count is not None:
                self.setCount(count)

    def updateResult(self, status: Any):
        if status is not None:
            if isinstance(status, AuthStatus):
                if not status.authorised:
                    self.popup.error(status.msg)
            elif isinstance(status, Result):
                if status.result == Result.ERROR:
                    self.popup.error(status.msg)
                elif status.result == Result.WARNING:
                    self.popup.warning(status.msg, **status.details)
                else:
                    self.popup.info(status.msg, **status.details)
            else:
                self.popup.info(status)

    def updateFinish(self):
        pass

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
        _url = self.url.getText()

        if _webdriver == 'Firefox':
            _webdriver_exe = paths.get_firefoxdriver()
        else:
            _webdriver_exe = paths.get_chromedriver()

        self.seleniumEngine.launch(_webdriver, _webdriver_exe, _url)

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
        parse_from = self.parseFromCombo.getCurrentText()

        if parse_from == 'History':
            _element = self.history.getCurrentText()
            origin = state['history'][_element]
        else:
            origin = parse_from

        _engine = self.engineSelect.getCurrentText()

        if _engine == 'Selenium':
            by = self.findParams.getCurrentText()
            element = self.elementParams.getText()
            target = self.targetCombo.getCurrentText()

            element = Element.from_text(f"{by}={element}")

            self.seleniumEngine.find(origin=origin,
                                     element=element,
                                     target=target)
        else:
            tagParam = self.tagElem.getCurrentText()
            classParam = self.classParam.getText()
            idParam = self.idParam.getText()

            target = self.targetCombo.getCurrentText()

            if classParam == '':
                _class = None
            else:
                _class = classParam

            if idParam == '':
                _id = None
            else:
                _id = idParam

            element = Element(tag_name=tagParam,
                              class_name=_class,
                              id=_id)

            self.bsEngine.refresh_soup_from_selenium_engine(self.seleniumEngine)

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
        _attr = self.attrsCombo.getCurrentText()

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

    def onStoreElement(self):
        run_thread(threadpool=self.threadpool,
                   function=self.storeElement,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def setActiveFromHistory(self, _progress):
        history_element_name = self.history.getCurrentText()

        if history_element_name:
            _engine = self.selectEngine()

            _engine.set_active_from_history(history_element_name)
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
