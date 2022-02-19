# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
MAIN FILE
Handles the web instanciation and logic.
"""

import os
import flask

import dash
from com.authentification import EncryptedAuth
from dash.dependencies import Input, Output


import logs

import update_data

# Import the config file
from access import ConfigAccess

# SSL_CONTEXT = myAccessConfig.getSSLContext()

from wrapper_dash import vue_index, vue_home
from wrapper_dash import vue_dashboard_home
from wrapper_dash import vue_test

from wrapper_dash.facilitator_dash.tools import getUsername

# Dash Application
class AppDash:
    """Framework Dash.
    Here is handled the web part of the application."""

    # TODO: use environment
    def __init__(self):
        external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
        environment = os.environ.get("ENVIRONMENT")

        self.app = dash.Dash(
            __name__,
            external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=True,
            server=flask.Flask(__name__),
        )
        self.addAuthentification(self.app)

        self.vueIndex = vue_index.AppDash(self.app)
        self.vueHome = vue_home.AppDash(self.app)
        self.vueDashboardHome = vue_dashboard_home.AppDash(self.app)
        self.vueTest = vue_test.AppDash(self.app)

        # self.app.css.append_css({"external_url": "static/main.css"})

    def setVueIndex(self):
        self.app.layout = self.vueIndex.setDefaultVue()

    # You can add a vue by inserting the desirated vue and path here
    def setCallback(self):
        @self.app.callback(
            Output("default-page-content", "children"), Input("default-url", "pathname")
        )
        def display_page(pathname):
            username = getUsername()
            dash.callback_context.response.set_cookie("username", username)
            if pathname == "/":
                return self.vueIndex.setThisVue()
            elif pathname == "/home":
                return self.vueHome.setThisVue()
            elif pathname == "/dashhome":
                update_data.updateAll(username)
                return self.vueDashboardHome.setThisVue()
            elif pathname == "/reset":
                update_data.removeAllDataForUser(username)
                return "All data has been reseted :)"
            elif pathname == "/test":
                return self.vueTest.setThisVue()
            else:
                return "404 Page not found."

    def set_default_page(self):
        self.setVueIndex()
        self.setCallback()

    def run(self, debug=True, ssl_context=None, *args, **kwargs):
        self.app.run_server(debug=debug, ssl_context=ssl_context, *args, **kwargs)
        # self.app.run_server(debug=False, ssl_context=SSL_CONTEXT)
        # self.app.run_server(debug=True, ssl_context="adhoc")

    def addAuthentification(self):
        VALID_USERNAME_PASSWORD_PAIRS = ConfigAccess.users()
        EncryptedAuth(self.app, VALID_USERNAME_PASSWORD_PAIRS)


def createDashApp():
    logs.formatAndDisplay(
        "Application creation...", "-#", logs.Position.CENTER, to_highlight=True
    )
    dash_app = AppDash()
    dash_app.set_default_page()
    return dash_app


if __name__ == "__main__":
    """Launch the application by command line:
    pipenv run python app.py"""
    logs.startLogs()
    logs.formatAndDisplay(
        "Launch main sccript", "+#", logs.Position.CENTER, to_highlight=True
    )
    dash_app = createDashApp()
    dash_app.run()
