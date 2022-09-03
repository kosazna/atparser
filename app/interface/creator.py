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
    elementAdded = pyqtSignal()

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
        self.history.addItems(state.history.keys())
        self.buttonAddElement.subscribe(self.onAddElement)
        self.history.subscribe(self.onHistoryComboChange)

    def getParams(self, key: Optional[str] = None):
        params = {
            'name': self.elName.getText() or None,
            'tag_name': self.elTag.getCurrentText() or None,
            'class_name': self.elClass.getText() or None,
            'id': self.elId.getText() or None,
            'xpath': self.elXpath.getText() or None,
            'css_selector': self.elCss.getText() or None,
            'attribute': self.elAttribute.getText() or None,
            'default': self.elDefault.getText() or None,
            'many': self.elMany.isChecked()
        }

        return params if key is None else params.get(key)

    def onAddElement(self):
        params = self.getParams()

        element = Element(**params)

        state.elements.update({str(element): element})

        self.elementAdded.emit()

    def onHistoryComboChange(self):
        _el_name = self.history.getCurrentText()
        _el: Element = state.parsing_elems.get(_el_name)

        if _el is not None:
            props = _el.to_dict()

            self.elCss.setText(props.get('css_selector', ''))
            self.elTag.setCurrentText(props.get('tag_name', ''))
            self.elClass.setText(props.get('class_name', ''))
            self.elId.setText(props.get('id', ''))
            self.elXpath.setText(props.get('xpath', ''))
        
        self.parseCssSelector()

    def parseCssSelector(self):
        css_selector = self.getParams('css_selector')

        if '.' in css_selector:
            splitted = css_selector.split('.')

            if splitted:
                tag = splitted[0]
                if tag in MOST_COMMON_HTML_TAGS:
                    self.elTag.setCurrentText(tag)
            
                if len(splitted) > 1:
                    string = ' '.join(splitted[1:])
                    self.elClass.setText(string)


        if '#' in css_selector:
            splitted = css_selector.split('#')

            if splitted:
                tag = splitted[0]
                if tag in MOST_COMMON_HTML_TAGS:
                    self.elTag.setCurrentText(tag)
            
                if len(splitted) > 1:
                    string = ' '.join(splitted[1:])
                    self.elId.setText(string)

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
