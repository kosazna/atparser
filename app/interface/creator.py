# -*- coding: utf-8 -*-
import sys
from typing import Any, Optional, Tuple

from at.auth.client import AuthStatus
from at.gui import *
from at.logger import log
from at.result import Result
from at.web import Element
from atparser.app.core import BeautifulSoupEngine, SeleniumEngine
from atparser.app.settings import *
from atparser.app.utils import paths, state
from PyQt5.QtCore import Qt, QThreadPool, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

# When setting fixed width to QLineEdit ->
# -> add alignment=Qt.AlignLeft when adding widget to layout


class CreatorTab(AtWidget):
    def __init__(self,
                 size: Tuple[Optional[int]] = (None, None),
                 parent: Optional[QWidget] = None,
                 *args,
                 **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.initUi(size)

    def setupUi(self, size):
        set_size(widget=self, size=size)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(2, 4, 2, 0)

        self.history = ComboInput(label='History',
                                  labelsize=LABELSIZE,
                                  combosize=HISTORYSIZE,
                                  parent=self)
        self.elName = StrInput(label='Name',
                               labelsize=LABELSIZE,
                               parent=self)
        self.elCss = StrInput(label='Css',
                              labelsize=LABELSIZE,
                              parent=self)
        self.elTag = ComboInput(label='Tag',
                                items=MOST_COMMON_HTML_TAGS,
                                labelsize=LABELSIZE,
                                combosize=COMBOSIZE,
                                parent=self)
        self.elClass = StrInput(label='Class',
                                labelsize=LABELSIZE,
                                parent=self)
        self.elId = StrInput(label='Id',
                             labelsize=LABELSIZE,
                             parent=self)
        self.elXpath = StrInput(label='Xpath',
                                labelsize=LABELSIZE,
                                parent=self)
        self.elAttribute = StrInput(label='Attribute',
                                    labelsize=LABELSIZE,
                                    parent=self)
        self.elDefault = StrInput(label='Default',
                                  labelsize=LABELSIZE,
                                  parent=self)
        self.elMany = CheckInput(label='Many',
                                 checked=False,
                                 parent=self)
        self.buttonAddElement = Button(label='Add Element',
                                       size=BUTTONSIZE_HIGHLIGHT,
                                       parent=self)

        mainLayout.addWidget(self.history)
        mainLayout.addWidget(self.elName)
        mainLayout.addWidget(self.elCss)
        mainLayout.addWidget(self.elTag)
        mainLayout.addWidget(self.elClass)
        mainLayout.addWidget(self.elId)
        mainLayout.addWidget(self.elXpath)
        mainLayout.addWidget(self.elAttribute)
        mainLayout.addWidget(self.elDefault)
        mainLayout.addWidget(self.elMany, alignment=Qt.AlignRight)
        mainLayout.addWidget(HLine(), stretch=2, alignment=Qt.AlignTop)
        mainLayout.addWidget(self.buttonAddElement, alignment=Qt.AlignHCenter)

        self.setLayout(mainLayout)

    def initUi(self, size: tuple):
        self.setupUi(size)
        self.history.addItems(state['history'].keys())

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


if __name__ == '__main__':
    cssGuide = paths.get_css(obj=True).joinpath("_style.css").read_text()
    SEGOE = QFont("Segoe UI", 9)

    app = QApplication(sys.argv)
    app.setFont(SEGOE)
    app.setStyle('Fusion')

    ui = CreatorTab(size=(600, None))
    ui.setStyleSheet(cssGuide)
    ui.show()

    sys.exit(app.exec_())
