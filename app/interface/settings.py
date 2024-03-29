# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from typing import Any, Optional, Tuple
from at.auth.client import AuthStatus, licensed
from at.gui import *
from at.gui.worker import run_thread
from at.logger import log
from at.result import Result
from at.io.utils import load_json, write_json
from atparser.app.utils.path import paths
from atparser.app.utils.state import state
# from PyQt5.QtCore import Qt, QThreadPool, pyqtSignal
# from PyQt5.QtGui import QFont
# from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

# When setting fixed width to QLineEdit ->
# -> add alignment=Qt.AlignmentFlag.AlignLeft when adding widget to layout


class SettingsTab(AtWidget):
    settingsChanged = pyqtSignal()
    serverStatusChanged = pyqtSignal(tuple)

    def __init__(self,
                 size: Tuple[Optional[int]] = (None, None),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.initUi(size)

    def setupUi(self, size):
        set_size(widget=self, size=size)

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 4, 2, 0)
        driverLayout = QHBoxLayout()
        labelLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        self.app = Label(icon='app',
                         label=state.appname,
                         parent=self)
        self.version = Label(icon='hash',
                             label=state.version,
                             parent=self)
        self.driverSelect = ComboInput(label="WebDriver",
                                       labelsize=(140, 24),
                                       combosize=(100, 24),
                                       items=('Firefox', 'Chrome'),
                                       parent=self)
        self.driverExist = StatusLabel(icon='hdd-network-fill',
                                       statussize=(110, 24),
                                       parent=self)
        self.delayLaunch = IntInput(label='Launch delay',
                                    labelsize=(140, 24),
                                    editsize=(100, 24),
                                    parent=self)
        self.delayUrlChange = IntInput(label='URL change delay',
                                       labelsize=(140, 24),
                                       editsize=(100, 24),
                                       parent=self)
        self.delayPaginator = IntInput(label='Paginator delay',
                                       labelsize=(140, 24),
                                       editsize=(100, 24),
                                       parent=self)
        self.saveButton = Button(label="Αποθήκευση Αλλαγών",
                                 size=(160, 26),
                                 parent=self)
        self.status = StatusButton(parent=self)

        labelLayout.addWidget(self.app)
        labelLayout.addWidget(self.version, stretch=2, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(labelLayout)
        layout.addWidget(HLine())
        driverLayout.addWidget(self.driverSelect)
        driverLayout.addWidget(self.driverExist,
                               stretch=2,
                               alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(driverLayout)
        layout.addWidget(self.delayLaunch, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.delayUrlChange, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.delayPaginator, alignment=Qt.AlignmentFlag.AlignLeft)

        buttonLayout.addWidget(self.saveButton, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(buttonLayout)

        layout.addWidget(HLine())
        layout.addWidget(self.status, stretch=2, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)

    def initUi(self, size: tuple):
        self.setupUi(size)
        self.driverSelect.setCurrentText(state.webdriver)
        self.delayLaunch.setText(str(state.launch_delay))
        self.delayUrlChange.setText(str(state.urlchange_delay))
        self.delayPaginator.setText(str(state.paginator_delay))
        self.checkDrivers()
        self.driverSelect.subscribe(self.onDriverChange)
        self.saveButton.subscribe(self.onSave)

    def checkDrivers(self):
        if self.driverSelect.getCurrentText() == 'chrome':
            if paths.get_chromedriver(True).exists():
                self.driverExist.changeStatus("Driver exists", 'statusOk')
            else:
                self.driverExist.changeStatus("No Driver", 'statusError')
        else:
            if paths.get_firefoxdriver(True).exists():
                self.driverExist.changeStatus("Driver exists", 'statusOk')
            else:
                self.driverExist.changeStatus("No Driver", 'statusError')

    def onDriverChange(self):
        self.pickedDriver = self.driverSelect.getCurrentText()
        self.checkDrivers()

    def onSave(self):
        state.webdriver = self.driverSelect.getCurrentText()

        state.launch_delay = self.delayLaunch.getInt()
        state.urlchange_delay = self.delayUrlChange.getInt()
        state.paginator_delay = self.delayPaginator.getInt()

        self.settingsChanged.emit()

        self.popup.info("Οι ρυθμίσεις αποθηκεύτηκαν")


if __name__ == '__main__':
    cssGuide = paths.get_css(obj=True).joinpath("_style.css").read_text()
    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = SettingsTab(size=(600, None))
    ui.setStyleSheet(cssGuide)
    ui.show()

    sys.exit(app.exec_())
