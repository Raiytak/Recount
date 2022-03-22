from dash import dcc, html

from .components.css_style import *
from .abstract_vue import AbstractVue
from .components import link

__all__ = ["Index"]


class Index(AbstractVue):
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
            ],
            className="nav-links",
        )
        tools = html.Div(id="tools")
        nav_div = html.Nav(children=[logo_div, links_div, tools], style=spaceBetween)
        page_content = html.Div(id="page-content")
        whole_page = html.Div(children=[nav_div, page_content])
        return whole_page
