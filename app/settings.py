# -*- coding: utf-8 -*-

from at.utils import user
from pathlib import Path

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

if Path(f"C:/Users/{USERNAME}/.{APPNAME}/static/{ICONNAME}").exists():
    APPICON = f"C:/Users/{USERNAME}/.{APPNAME}/static/{ICONNAME}"
else:
    APPICON = ICONNAME

FIND_PARAMS = ('class',
               'id',
               'xpath',
               'css',
               'tag')
