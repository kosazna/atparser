# -*- coding: utf-8 -*-

from typing import Optional
from at.path import PathEngine
from pathlib import Path
from atktima.app.settings import *


class WebParserPaths(PathEngine):

    def __init__(self, appname: str = APPNAME):
        super().__init__(appname=appname)


paths = WebParserPaths(appname=APPNAME)
