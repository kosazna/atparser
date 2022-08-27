# -*- coding: utf-8 -*-
import sys
from typing import Any, Optional, Tuple

from at.gui import *
from at.logger import log
from at.result import Result
from at.web import Element, ElementStore
from atparser.app.settings import *
from atparser.app.utils import paths, state
from PyQt5.QtCore import Qt
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
        self.element_store = ElementStore()

    def setupUi(self, size):
        set_size(widget=self, size=size)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(2, 4, 2, 0)

        buttonLayout = QHBoxLayout()

        self.elements = ComboInput(label='Element',
                                   labelsize=LABELSIZE,
                                   combosize=HISTORYSIZE,
                                   parent=self)
        self.caterory = ComboInput(label='Category',
                                   labelsize=LABELSIZE,
                                   combosize=COMBOSIZE_XL,
                                   items=ELEMENT_CATEGORIES,
                                   parent=self)
        self.childrenElem = ListWidget(label='Children',
                                       widgetsize=LISTSIZE,
                                       parent=self)

        self.filepath = FileOutput(label='Filepath',
                                   labelsize=LABELSIZE,
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
        mainLayout.addWidget(self.childrenElem)
        mainLayout.addWidget(self.buttonAddConfig, alignment=Qt.AlignRight)
        mainLayout.addWidget(HLine(), stretch=2, alignment=Qt.AlignTop)
        mainLayout.addWidget(self.filepath)
        mainLayout.addWidget(self.buttonSerializer, alignment=Qt.AlignHCenter)

        self.setLayout(mainLayout)

    def initUi(self, size: tuple):
        self.setupUi(size)
        self.elements.addItems(state['history'].keys())
        self.buttonAddConfig.subscribe(self.onAddToConfig)
        self.buttonSerializer.subscribe(lambda : self.runThread(self.onSerialize))

    def getParams(self, key: Optional[str] = None):
        params = {
            'element': self.elements.getCurrentText(),
            'category': self.caterory.getCurrentText(),
            'children': self.childrenElem.getCheckState(),
            'filepath': self.filepath.getText()
        }

        return params if key is None else params.get(key)

    def onAddToConfig(self):
        params = self.getParams()

        element: Element = state['elements'][params.get('element')]
        category = params.get('category')
        children = [state['elements'][el] for el in params.get('children')]

        if children:
            if len(children) == 1:
                element.children = children[0]
            else:
                element.children = children

        self.element_store.__dict__[category] = element

    def onSerialize(self, _progress):
        filepath = self.getParams('filepath')
        self.element_store.to_json_config(filepath=filepath)

        return Result.success('Config file created')


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
