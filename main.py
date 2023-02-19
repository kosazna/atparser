# -*- coding: utf-8 -*-
import ctypes
import sys

from at.gui.utils import get_dpi
from at.logger import log
# from PyQt5.QtGui import QFont, QIcon
# from PyQt5.QtWidgets import QApplication

from at.gui.components import QApplication, QFont, QIcon



if __name__ == "__main__":
    from atparser.app.settings import *
    from atparser.app.utils.path import paths

    log.set_mode("GUI")
    log.set_exception_handling(logger_filepath=paths.get_logger(),
                               logger_name=APPNAME)
    
    from atparser.app import WebParserUI

    appid = 'com.aztool.atparser.app'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

    app = QApplication(sys.argv)

    if get_dpi(app) < 120:
        SEGOE = QFont(FONT, FONTSIZE)
    else:
        SEGOE = QFont(FONT, FONTSIZE - 1)

    app.setWindowIcon(QIcon(APPICON))
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = WebParserUI(size=APPSIZE)
    ui.show()

    log.flush()

    sys.exit(app.exec())
