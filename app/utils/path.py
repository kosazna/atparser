# -*- coding: utf-8 -*-

from typing import Optional
from at.path import PathEngine
from pathlib import Path
from atparser.app.settings import *


class WebParserPaths(PathEngine):

    def __init__(self, appname: str = APPNAME):
        super().__init__(appname=appname)

    def get_chromedriver(self, obj: bool = False):
        _path = self.get_app(obj=True).joinpath("chromedriver.exe")

        if obj:
            return _path
        return _path.as_posix()

    def get_firefoxdriver(self, obj: bool = False):
        _path = self.get_app(obj=True).joinpath("geckodriver.exe")

        if obj:
            return _path
        return _path.as_posix()


paths = WebParserPaths(appname=APPNAME)
