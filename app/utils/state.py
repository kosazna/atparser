# -*- coding: utf-8 -*-

from at.state import State
from atparser.app.settings import *


state = State()
state.set({'appname': APPNAME,
           'version': VERSION,
           'debug': DEBUG,
           'webdriver': 'Firefox',
           'paginator_delay': PAGINATOR_DELAY,
           'launch_delay': LAUNCH_DELAY,
           'urlchange_delay': URLCHANGE_DELAY,
           'history': {}})
