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


class SerializerTab(AtWidget):
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

        self.elements = ComboInput(label='Element',
                                   labelsize=LABELSIZE,
                                   combosize=HISTORYSIZE,
                                   parent=self)
        self.caterory = ComboInput(label='Category',
                                   labelsize=LABELSIZE,
                                   combosize=COMBOSIZE_XL,
                                   items=('interaction',
                                          'filters',
                                          'data'),
                                   parent=self)
        self.subcaterory = StrInput(label='Subcategory',
                                    labelsize=LABELSIZE,
                                    parent=self)
        self.childrenElem = ListWidget(label='Children',
                                       widgetsize=LISTSIZE,
                                       parent=self)

        self.buttonAddConfig = Button(label='Add to config',
                                      size=BUTTONSIZE_REGULAR_XL,
                                      parent=self)
        self.buttonSerializer = Button(label='Serialize',
                                       size=BUTTONSIZE_HIGHLIGHT,
                                       color='blue',
                                       parent=self)

        mainLayout.addWidget(self.elements)
        mainLayout.addWidget(self.caterory)
        mainLayout.addWidget(self.subcaterory)
        mainLayout.addWidget(self.childrenElem)
        mainLayout.addWidget(self.buttonAddConfig)
        mainLayout.addWidget(self.buttonSerializer)

        mainLayout.addWidget(HLine(), stretch=2, alignment=Qt.AlignTop)

        self.setLayout(mainLayout)

    def initUi(self, size: tuple):
        self.setupUi(size)
        self.elements.addItems(state['history'].keys())

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

    ui = SerializerTab(size=(600, None))
    ui.setStyleSheet(cssGuide)
    ui.show()

    sys.exit(app.exec_())
