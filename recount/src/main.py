# -*- coding: utf-8 -*-
""" 
Handles web instanciation and logic.
"""
from dash import Dash
from security.authentification import *

import logs
from website import *
from accessors.file_management import AssetManager


def createDashApp(*args, **kwargs) -> Dash:
    default_values = {
        "external_stylesheets": ["https://codepen.io/chriddyp/pen/bWLwgP.css"],
        "suppress_callback_exceptions": True,
        "assets_folder": str(AssetManager.ROOT),
    }
    for key, value in default_values.items():
        if not key in kwargs.keys():
            kwargs[key] = value

    logs.formatAndDisplay("Application creation...", "-#", logs.Position.CENTER)
    dash_app = Dash(*args, **kwargs)
    addAuthentification(dash_app)
    # setDefaultPage(dash_app)
    logs.formatAndDisplay("Application created!", "-#", logs.Position.CENTER)
    return dash_app


def runApp(app: Dash, *args, **kwargs):
    default_values = {
        "debug": True,
        "ssl_context": None,  # can be set as ssl_context="adhoc" or setting it manually
    }
    for key, value in default_values:
        if not key in kwargs.keys():
            kwargs[key] = value

    app.run_server(*args, **kwargs)
