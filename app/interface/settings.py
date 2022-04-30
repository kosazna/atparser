# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from typing import Any, Optional, Tuple
from at.auth.client import AuthStatus, licensed
from at.gui.components import *
from at.gui.utils import set_size
from at.gui.worker import run_thread
from at.logger import log
from at.result import Result
from at.io.utils import load_json, write_json
from atparser.app.utils import paths, state
from PyQt5.QtCore import Qt, QThreadPool, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

# When setting fixed width to QLineEdit ->
# -> add alignment=Qt.AlignLeft when adding widget to layout


class SettingsTab(QWidget):
    settingsChanged = pyqtSignal()
    serverStatusChanged = pyqtSignal(tuple)

    def __init__(self,
                 size: Tuple[Optional[int]] = (None, None),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.setupUi(size)
        self.threadpool = QThreadPool(parent=self)
        self.popup = Popup(state['appname'])

        self.driverSelect.subscribe(self.onDriverChange)
        self.saveButton.subscribe(self.onSave)

    def setupUi(self, size):
        set_size(widget=self, size=size)

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 4, 2, 0)
        driverLayout = QHBoxLayout()
        labelLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        self.app = Label(icon='app',
                         label=state['appname'],
                         parent=self)
        self.version = Label(icon='hash',
                             label=state['version'],
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

        self.driverSelect.setCurrentText(state['webdriver'])
        self.delayLaunch.setText(str(state['launch_delay']))
        self.delayUrlChange.setText(str(state['urlchange_delay']))
        self.delayPaginator.setText(str(state['paginator_delay']))

        self.checkDrivers()

        labelLayout.addWidget(self.app)
        labelLayout.addWidget(self.version, stretch=2, alignment=Qt.AlignLeft)
        layout.addLayout(labelLayout)
        layout.addWidget(HLine())
        driverLayout.addWidget(self.driverSelect)
        driverLayout.addWidget(self.driverExist,
                               stretch=2, alignment=Qt.AlignLeft)
        layout.addLayout(driverLayout)
        layout.addWidget(self.delayLaunch, alignment=Qt.AlignLeft)
        layout.addWidget(self.delayUrlChange, alignment=Qt.AlignLeft)
        layout.addWidget(self.delayPaginator, alignment=Qt.AlignLeft)

        buttonLayout.addWidget(self.saveButton, alignment=Qt.AlignRight)
        layout.addLayout(buttonLayout)

        layout.addWidget(HLine())
        layout.addWidget(self.status, stretch=2, alignment=Qt.AlignBottom)

        self.setLayout(layout)

    def updateProgress(self, metadata: dict):
        if metadata:
            progress_now = metadata.get('pbar', None)
            progress_max = metadata.get('pbar_max', None)
            status = metadata.get('status', None)

            if progress_now is not None:
                self.progress.setValue(progress_now)
            if progress_max is not None:
                self.progress.setMaximum(progress_max)
            if status is not None:
                self.status.disable(str(status))

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
        state['webdriver'] = self.driverSelect.getCurrentText()

        state['launch_delay'] = self.delayLaunch.getInt()
        state['urlchange_delay'] = self.delayUrlChange.getInt()
        state['paginator_delay'] = self.delayPaginator.getInt()

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
