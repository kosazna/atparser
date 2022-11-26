# -*- coding: utf-8 -*-
import ctypes
import sys

from at.gui.utils import get_dpi
from at.logger import log
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    log.set_mode("GUI")

    from atparser.app import WebParserUI
    from atparser.app.settings import *

    appid = 'com.aztool.atparser.app'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

    if get_dpi() < 120:
        SEGOE = QFont(FONT, FONTSIZE)
    else:
        SEGOE = QFont(FONT, FONTSIZE - 1)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(APPICON))
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = WebParserUI(size=APPSIZE)
    ui.show()

    log.flush()

    sys.exit(app.exec_())
