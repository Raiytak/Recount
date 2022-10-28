from dash import dcc, html


from .css_style import *

__all__ = ["RecountLinks"]


class RecountLinks:
    def __init__(self, index_path, *args, **kwargs):
        self.index_path = index_path

    def home(self) -> dcc.Link:
        button = html.Button("HomeVue", className="nav-button")
        home_page = dcc.Link(button, href=self.index_path.HOME)
        return home_page

    def category(self) -> dcc.Link:
        button = html.Button("Category", className="nav-button")
        categories = dcc.Link(button, href=self.index_path.CATEGORY)
        return categories

    def dashboardHome(self) -> dcc.Link:
        button = html.Button("Dashboard", className="nav-button")
        dashhome = dcc.Link(button, href=self.index_path.DASHHOME)
        return dashhome

    def notebook(self) -> dcc.Link:
        button = html.Button("Notebook", className="nav-button")
        notebook = dcc.Link(button, href=self.index_path.NOTEBOOK)
        return notebook
