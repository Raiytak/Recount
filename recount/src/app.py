# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
MAIN FILE
Handles the web instanciation and logic.
"""

import flask

import dash
from com.authentification import EncryptedAuth
from dash.dependencies import Input, Output

import logs
import pipeline
from website import *
from access import ConfigAccess

# SSL_CONTEXT = myAccessConfig.getSSLContext()

from recount_tools import getUsername

# Dash Application
class AppDash:
    """Framework Dash.
    Here is handled the web part of the application."""

    # TODO: use environment
    def __init__(self):
        external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

        self.app = dash.Dash(
            __name__,
            external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=True,
            server=flask.Flask(__name__),
        )
        self.addAuthentification()

        # self.vueIndex = vue_index.AppDash(self.app)
        # self.vueHome = vue_home.AppDash(self.app)
        # self.vueDashboardHome = vue_dashboard_home.AppDash(self.app)
        # self.vueTest = vue_test.AppDash(self.app)

        # self.app.css.append_css({"external_url": "static/main.css"})

    def setVue(self, vue):
        self.app.layout = vue

    # You can add a vue by inserting the desirated vue and path here
    def setCallback(self):
        @self.app.callback(Output("page-content", "children"), Input("url", "pathname"))
        def display_page(pathname):
            username = getUsername()
            user_pipeline = pipeline.UpdateDatabase(
                username, ConfigAccess.database_config
            )
            dash.callback_context.response.set_cookie("username", username)
            if pathname == "/":
                return None
            elif pathname == "/home":
                return HomePage.vue
            # elif pathname == "/dashhome":
            #     user_pipeline.updateData()
            #     return self.vueDashboardHome.setThisVue()
            # elif pathname == "/reset":
            #     update_data.removeAllDataForUser(username)
            #     return "All data has been reseted :)"
            # elif pathname == "/test":
            #     return self.vueTest.setThisVue()
            else:
                return "404 Page not found."

    def setDefaultPage(self):
        self.setVue(IndexPage.vue)
        self.setCallback()

    def run(self, debug=True, ssl_context=None, *args, **kwargs):
        self.app.run_server(debug=debug, ssl_context=ssl_context, *args, **kwargs)
        # self.app.run_server(debug=False, ssl_context=SSL_CONTEXT)
        # self.app.run_server(debug=True, ssl_context="adhoc")

    def addAuthentification(self):
        VALID_USERNAME_PASSWORD_PAIRS = ConfigAccess.users
        EncryptedAuth(self.app, VALID_USERNAME_PASSWORD_PAIRS)


def createDashApp():
    logs.formatAndDisplay("Application creation...", "-#", logs.Position.CENTER)
    dash_app = AppDash()
    dash_app.setDefaultPage()
    logs.formatAndDisplay("Application created!", "-#", logs.Position.CENTER)
    return dash_app
