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

        self.setActiveFromHistory = Button(label='Set active',
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
        historyLayout.addWidget(self.setActiveFromHistory)
        layout.addLayout(historyLayout)
        layout.addWidget(HLine())
        layout.addWidget(self.targetCombo)
        paramsLayout.addWidget(self.findParams)
        paramsLayout.addWidget(self.elementParams, stretch=2)
        layout.addLayout(paramsLayout)
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
            self.history.addItems(state['history'].keys())


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
