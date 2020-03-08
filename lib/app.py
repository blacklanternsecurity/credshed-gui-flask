#!/usr/bin/env python3

# by TheTechromancer

from .api import *
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# create the application object
gui = Flask('credshed-gui')

base_api_url = '/api'

# /api gets routed to credshed api
app = DispatcherMiddleware(
    gui, 
    {
        '/api': api
    }
)