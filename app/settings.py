# -*- coding: utf-8 -*-

from pathlib import Path

from at.utils import user

APPNAME = "webparser"
VERSION = "0.1.1"
DEBUG = False
USERNAME = user()
FONT = "Segoe UI"
FONTSIZE = 9
ICONNAME = "webparser.ico"

LAUNCH_DELAY = 4
URLCHANGE_DELAY = 3
PAGINATOR_DELAY = 2

WIDGETHEIGHT = 24
LABELSIZE = (70, WIDGETHEIGHT)
COMBOSIZE = (120, WIDGETHEIGHT)
COMBOSIZE_XL = (120, WIDGETHEIGHT)
HISTORYSIZE = (500, WIDGETHEIGHT)
BUTTONSIZE_REGULAR = (100, 24)
BUTTONSIZE_REGULAR_XL = (150, 24)
BUTTONSIZE_HIGHLIGHT = (200, 30)
LISTSIZE = (None, 300)
STATUSSIZE = (160, 22)
TABSIZE = (700, None)
CONSOLESIZE = (700, None)
APPSIZE = (None, 700)

if Path(f"C:/Users/{USERNAME}/.{APPNAME}/static/{ICONNAME}").exists():
    APPICON = f"C:/Users/{USERNAME}/.{APPNAME}/static/{ICONNAME}"
else:
    APPICON = ICONNAME

ELEMENT_CATEGORIES = ('cookies',
                      'paginator',
                      'filters',
                      'data')

FIND_PARAMS = ('css selector',
               'class name',
               'tag name',
               'id',
               'xpath',
               'link text',
               'partial link text')

MOST_COMMON_HTML_TAGS = ('',
                         'div',
                         'span',
                         'a',
                         'p',
                         'img',
                         'ol',
                         'ul',
                         'li',
                         'h1',
                         'h2',
                         'h3',
                         'h4',
                         'h5',
                         'h6',
                         'title',
                         'b',
                         'i',
                         'u',
                         'link',
                         'table',
                         'tr',
                         'th',
                         'td',
                         'form',
                         'input',
                         'option')
