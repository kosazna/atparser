# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from typing import Any, Optional, Tuple
from at.auth.client import AuthStatus, licensed
from at.gui.components import *
from at.gui.utils import VERTICAL, set_size
from at.gui.worker import run_thread
from at.io.copyfuncs import copy_pattern_from_files
from at.logger import log
from at.result import Result
from atparser.app.settings import *
from atparser.app.utils import paths, state
from atparser.app.core import SeleniumEngine
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
        self.engine = SeleniumEngine()
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

    def setupUi(self, size):
        set_size(widget=self, size=size)

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 4, 2, 0)

        urlLayout = QHBoxLayout()
        engineChecksLayout = QVBoxLayout()
        paramsLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        historyLayout = QHBoxLayout()
        parseFromLayout = QHBoxLayout()
        actionElemLayout = QVBoxLayout()
        interactionLayout = QVBoxLayout()
        attrsLayout = QHBoxLayout()

        self.url = StrInput(label='URL',
                            parent=self)

        self.buttonLaunch = Button(label='Launch',
                                   parent=self)

        self.engineCombo = ComboInput(label='Engine',
                                      items=('selenium', 'bs4'),
                                      parent=self)

        self.parseFromCombo = ComboInput(label='Parse from',
                                         items=('Driver',
                                                'Active element',
                                                'History'),
                                         parent=self)
        self.parseFromStatus = StatusLabel(statussize=(340, 22),
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

        self.findParams = ComboInput(label='Params',
                                     items=FIND_PARAMS,
                                     combosize=(80, 24),
                                     parent=self)

        self.elementParams = StrInput(parent=self)

        self.attrsCombo = ComboInput(label='Attrs',
                                     combosize=(200, 24),
                                     parent=self)

        self.buttonGetAttribute = Button(label='Get attribute',
                                         size=(180, 24),
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
        self.buttonScroll = Button(label='Scroll down',
                                   size=(150, 24),
                                   parent=self)

        self.status = StatusButton(parent=self)

        self.parseFromStatus.setText('Driver')
        self.url.setText(
            "https://www.skroutz.gr/c/40/kinhta-thlefwna.html?from=families")

        urlLayout.addWidget(self.url)
        urlLayout.addWidget(self.buttonLaunch)
        layout.addLayout(urlLayout)
        layout.addWidget(HLine())
        parseFromLayout.addWidget(self.parseFromCombo)
        parseFromLayout.addWidget(self.parseFromStatus, stretch=2)
        engineChecksLayout.addWidget(self.engineCombo)
        engineChecksLayout.addLayout(parseFromLayout)
        layout.addLayout(engineChecksLayout)
        historyLayout.addWidget(self.history)
        historyLayout.addWidget(self.buttonSetActiveFromHistory)
        layout.addLayout(historyLayout)
        layout.addWidget(HLine())
        layout.addWidget(self.targetCombo)
        paramsLayout.addWidget(self.findParams)
        paramsLayout.addWidget(self.elementParams, stretch=2)
        layout.addLayout(paramsLayout)
        layout.addWidget(HLine())
        attrsLayout.addWidget(self.attrsCombo)
        attrsLayout.addWidget(self.buttonGetAttribute)
        layout.addLayout(attrsLayout)
        layout.addWidget(HLine())
        interactionLayout.addWidget(self.buttonClick)
        interactionLayout.addWidget(self.buttonScroll)
        actionElemLayout.addWidget(self.buttonSetActive)
        actionElemLayout.addWidget(self.buttonStore)
        buttonLayout.addWidget(self.buttonFind, alignment=Qt.AlignCenter)
        buttonLayout.addLayout(actionElemLayout)
        buttonLayout.addLayout(interactionLayout)
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

    def onLaunch(self):
        _webdriver = state['webdriver']
        _url = self.url.getText()

        if _webdriver == 'Firefox':
            _webdriver_exe = paths.get_firefoxdriver()
        else:
            _webdriver_exe = paths.get_chromedriver()

        self.engine.launch(_webdriver, _webdriver_exe, _url)

    def onParseFromChange(self):
        combo_text = self.parseFromCombo.getCurrentText()

        if combo_text == 'Driver':
            self.parseFromStatus.setText('Driver')
            self.history.clearItems()
        elif combo_text == 'Active element':
            self.parseFromStatus.setText(self.engine.active_element_name)
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

        by = self.findParams.getCurrentText()
        element = self.elementParams.getText()
        target = self.targetCombo.getCurrentText()

        self.engine.find(origin=origin,
                         by=by,
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

        texts = self.engine.get_attribute(_attr)

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
        self.engine.set_active()
        self.attrsCombo.clearItems()
        self.attrsCombo.addItems(self.engine.active_element_attrs)

    def onSetActiveElement(self):
        run_thread(threadpool=self.threadpool,
                   function=self.setActiveElement,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def storeElement(self, _progress):
        self.engine.store_element()

    def onStoreElement(self):
        run_thread(threadpool=self.threadpool,
                   function=self.storeElement,
                   on_update=self.updateProgress,
                   on_result=self.updateResult,
                   on_finish=self.updateFinish)

    def setActiveFromHistory(self, _progress):
        history_element_name = self.history.getCurrentText()

        self.engine.set_active_from_history(history_element_name)

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
