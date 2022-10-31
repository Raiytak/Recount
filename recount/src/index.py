# -*- coding: utf-8 -*-
"""
Routing of the web application
"""

from dash import callback
import dash
from dash.dependencies import Input, Output

from web import *
from security import getUsername
from accessors.file_management import UserManager
from database_manager import DatabaseManager
from database.sql_db import Table, UserSqlTable
from dash_manager import DashManager
from excel_manager import ExcelManager

__all__ = ["IndexManager"]


class IndexPath:
    HOME = "/home"
    DASHHOME = "/dashhome"
    CATEGORY = "/category"
    NOTEBOOK = "/notebook"


class IndexManager:
    def __init__(self,):
        self.index_page = IndexPage(IndexPath)
        self.home_page = HomePage()
        self.dashboard_page = DashboardHomePage(
            Table.EXPENSE,
            UserManager,
            ExcelManager,
            UserSqlTable,
            DatabaseManager,
            DashManager,
        )
        self.category_page = CategoryHomePage()
        # self.notebook_page = NotebookHomePage()

    def setCallbacks(self):
        @callback(Output("page-content", "children"), Input("url", "pathname"))
        def display_page(pathname):
            username = getUsername()
            dash.callback_context.response.set_cookie("username", username)
            if pathname == "/":  # returns the default page
                # return None
                return self.home_page.vue
            elif pathname == IndexPath.HOME:
                return self.home_page.vue
            elif pathname == IndexPath.DASHHOME:
                return self.dashboard_page.vue
            # elif pathname == IndexPath.CATEGORY:
            #     return self.category_page.vue
            else:
                return "404 Page not found."

    def setMainLayout(self, dash_app: dash.Dash):
        dash_app.layout = self.index_page.vue
