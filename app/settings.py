# -*- coding: utf-8 -*-

from at.utils import user
from pathlib import Path

APPNAME = "webparser"
VERSION = "0.1.1"
DEBUG = False
USERNAME = user()
FONT = "Segoe UI"
FONTSIZE = 9
ICONNAME = "ktima.ico"

if Path(f"C:/Users/{USERNAME}/.ktima/static/{ICONNAME}").exists():
    APPICON = f"C:/Users/{USERNAME}/.ktima/static/{ICONNAME}"
else:
    APPICON = ICONNAME
