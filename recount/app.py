""" 
Handles web instanciation and logic.
"""
from dash import Dash
from src.security.authentification import *

import src.logs as logs
from src.web import *
from src.accessors.file_management import AssetManager
from src.index import IndexManager


def launchApp(*args, **kwargs):
    recount_app = createRecountApp()
    runApp(recount_app, *args, **kwargs)


def runApp(recount_app: Dash, *args, **kwargs):
    default_values = {
        "debug": True,
        "ssl_context": None,  # can be set as ssl_context="adhoc" or setting it manually
    }
    for key, value in default_values.items():
        if not key in kwargs.keys():
            kwargs[key] = value

    recount_app.run_server(*args, **kwargs)
    return recount_app


def createRecountServer(*args, **kwargs):
    recount_app = createRecountApp(*args, **kwargs)
    return recount_app.server


def createRecountApp(*args, **kwargs) -> Dash:
    default_values = {
        "external_stylesheets": ["https://codepen.io/chriddyp/pen/bWLwgP.css"],
        "suppress_callback_exceptions": True,
        "assets_folder": str(AssetManager.ROOT),
    }
    for key, value in default_values.items():
        if not key in kwargs.keys():
            kwargs[key] = value
    index_manager = IndexManager()

    logs.formatAndDisplay("Application creation...", "-#", logs.Position.CENTER)
    dash_app = Dash(*args, **kwargs)
    addAuthentification(dash_app)
    index_manager.setMainLayout(dash_app)
    index_manager.setCallbacks()
    logs.formatAndDisplay("Application created!", "-#", logs.Position.CENTER)
    return dash_app
