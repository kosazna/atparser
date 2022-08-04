# -*- coding: utf-8 -*-
import sys
from typing import Optional, Tuple

from at.gui.components import Console
from at.gui.utils import set_size
from at.logger import log
from atparser.app.utils import paths, state
from atparser.app.interface import SettingsTab, ParserTab, CreatorTab
from atparser.app.settings import *
from PyQt5.QtCore import Qt, QThreadPool, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QTabWidget,
                             QVBoxLayout, QWidget)


cssGuide = paths.get_css(obj=True).joinpath("_style.css").read_text()


class WebParserUI(QWidget):
    def __init__(self,
                 size: Tuple[Optional[int]] = (None, None),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(size)
        self.threadpool = QThreadPool(parent=self)
        self.parserTab.historyChanged.connect(self.onHistoryChanged)
    

    def setupUi(self, size):
        self.setObjectName("MainWidget")
        self.setStyleSheet(cssGuide)
        self.setWindowTitle(f"{state['appname']}")
        self.move(150, 150)

        set_size(widget=self, size=size)

        self.appLayout = QHBoxLayout()

        self.console = Console(size=(800, None), parent=self)

        self.tabs = QTabWidget(parent=self)
        self.tabs.setDocumentMode(True)

        self.settingsTab = SettingsTab(size=(700, None), parent=self)
        self.tabs.addTab(self.settingsTab, "Settings")
        self.parserTab = ParserTab(size=(700, None), parent=self)
        self.tabs.addTab(self.parserTab, "Parsers")
        self.creator = CreatorTab(size=(700, None), parent=self)
        self.tabs.addTab(self.creator, "Creator")
        # self.paradosiTab = ParadosiTab(size=(700, None), parent=self)
        # self.tabs.addTab(self.paradosiTab, "Παράδοση")
        # self.anartisiTab = AnartisiTab(size=(700, None), parent=self)
        # self.tabs.addTab(self.anartisiTab, "Ανάρτηση")
        # self.organizeTab = OrganizeTab(size=(700, None), parent=self)
        # self.tabs.addTab(self.organizeTab, "Οργάνωση")
        # self.miscTab = MiscTab(size=(700, None), parent=self)
        # self.tabs.addTab(self.miscTab, "Διάφορα")

        self.appLayout.addWidget(self.tabs)
        self.appLayout.addWidget(self.console)

        self.tabs.setCurrentIndex(0)

        self.setLayout(self.appLayout)

    @pyqtSlot()
    def onHistoryChanged(self):
        self.creator.history.clearItems()
        self.creator.history.addItems(state['history'].keys())

    # @pyqtSlot(tuple)
    # def onServerStatusChanged(self, status):
    #     self.filesTab.server.changeStatus(*status)

    # def check_auth(self):
    #     status, info = auth.is_licensed(category=state['meleti'])
    #     auth.change_user_auth(status)
    #     if status:
    #         log.success(f"{info} for {state['meleti']}")
    #     else:
    #         log.error(f"{info} for {state['meleti']}")


if __name__ == '__main__':

    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = WebParserUI(size=(None, 600))
    ui.show()

    sys.exit(app.exec_())
