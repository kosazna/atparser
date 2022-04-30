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
        self.setupUi(size)
        self.threadpool = QThreadPool(parent=self)
        self.popup = Popup(state['appname'])

    def setupUi(self, size):
        set_size(widget=self, size=size)

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 4, 2, 0)

        modesLayout = QHBoxLayout()
        checksLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        self.engineCombo = ComboInput(label='Engine',
                                      items=('selenium', 'bs4'),
                                      parent=self)

        self.driverCheck = CheckInput(label='Driver',
                                      checked=True,
                                      parent=self)

        self.activeElemCheck = CheckInput(label='Active element',
                                          checked=False,
                                          parent=self)

        self.activeElemsCheck = CheckInput(label='Active elements',
                                           checked=False,
                                           parent=self)

        self.historyCheck = CheckInput(label='From history',
                                       checked=False,
                                       parent=self)

        self.history = ComboInput(label='History',
                                  combosize=(400, 24),
                                  parent=self)

        self.originCombo = ComboInput(label='Origin',
                                      items=('single', 'multiple'),
                                      parent=self)

        self.targetCombo = ComboInput(label='Target',
                                      items=('single', 'multiple'),
                                      parent=self)

        self.findParams = StrSelector(label='Parameters',
                                      mapping=FIND_PARAMS,
                                      combosize=(100, 24),
                                      editsize=(500, 24),
                                      parent=self)

        self.buttonFind = Button(label='Find Element',
                                 color='blue',
                                 size=(200, 30),
                                 parent=self)
        self.buttonSetActive = Button(label='Set active',
                                      size=(150, 24),
                                      parent=self)
        self.buttonStore = Button(label='Store',
                                        size=(150, 24),
                                        parent=self)
        self.status = StatusButton(parent=self)

        layout.addWidget(self.engineCombo)
        layout.addWidget(HLine())
        checksLayout.addWidget(self.driverCheck)
        checksLayout.addWidget(self.activeElemCheck)
        checksLayout.addWidget(self.activeElemsCheck)
        checksLayout.addWidget(self.historyCheck)
        layout.addLayout(checksLayout)
        layout.addWidget(self.history)
        layout.addWidget(HLine())
        modesLayout.addWidget(self.originCombo)
        modesLayout.addWidget(self.targetCombo)
        layout.addLayout(modesLayout)
        layout.addWidget(self.findParams)
        layout.addWidget(HLine())
        buttonLayout.addWidget(self.buttonFind)
        buttonLayout.addWidget(self.buttonSetActive)
        buttonLayout.addWidget(self.buttonStore)
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
