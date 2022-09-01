# -*- coding: utf-8 -*-

from at.state import AppState
from atparser.app.settings import *

state = AppState(appname=APPNAME,
                 version=VERSION,
                 debug=DEBUG)

state.webdriver = 'Firefox'
state.launch_delay = LAUNCH_DELAY
state.urlchange_delay = URLCHANGE_DELAY
state.paginator_delay = PAGINATOR_DELAY
state.history = {}
state.elements = {}
state.config = {}
