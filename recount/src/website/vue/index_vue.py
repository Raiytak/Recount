from dash import dcc, html

from .components.css_style import *
from .abstract_vue import AbstractVue
from .components import link

__all__ = ["IndexVue"]


class IndexVue(AbstractVue):
    @property
    def vue(self):
        # represents the browser address bar and doesn't render anything
        url = dcc.Location(id="url", refresh=False)
        logo_div = html.Div(id="logo")
        links_div = html.Div(
            children=[
                url,
                link.RecountLinks.home,
                link.RecountLinks.dashboardHome,
                link.RecountLinks.notebookHome,
                link.RecountLinks.categoryHome,
            ],
            className="nav-links",
        )
        tools = html.Div(id="tools")
        nav_div = html.Nav(children=[logo_div, links_div, tools], style=spaceBetween)
        page_content = html.Div(id="page-content")

        # default_spinner = "default-spinner"
        # loading_page_content = html.Div(
        #     className="loading-spinner " + default_spinner,
        #     style={"display": "block"},
        #     children=[
        #         html.Div(className=default_spinner + "-rectangle-1"),
        #         html.Div(className=default_spinner + "-rectangle-2"),
        #         html.Div(className=default_spinner + "-rectangle-3"),
        #         html.Div(className=default_spinner + "-rectangle-4"),
        #         html.Div(className=default_spinner + "-rectangle-5"),
        #     ],
        # )
        whole_page = html.Div(children=[nav_div, page_content])
        return whole_page
