from dash import dcc, html

from .components.css_style import *
from .abstract_vue import AbstractVue
from .components.link import RecountLinks

__all__ = ["IndexVue"]


class IndexVue(AbstractVue):
    def __init__(self, index_path, *args, **kwargs):
        self.recount_links = RecountLinks(index_path)
        super().__init__(*args, **kwargs)

    @property
    def vue(self):
        url = dcc.Location(
            id="url", refresh=False
        )  # represents the browser address bar and doesn't render anything
        logo_div = html.Div(id="logo")
        links_div = html.Div(
            children=[
                url,
                self.recount_links.home(),
                self.recount_links.dashboardHome(),
                # self.recount_links.notebook(),
                # self.recount_links.category(),
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
