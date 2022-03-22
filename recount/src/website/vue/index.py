from dash import dcc, html

from .abstract_vue import AbstractVue
from .components import link

__all__ = ["Index"]


class Index(AbstractVue):
    @property
    def vue(self):
        # represents the browser address bar and doesn't render anything
        url = dcc.Location(id="url", refresh=False)
        page_content = html.Div(id="page-content")
        links_div = html.Nav(
            children=[url, link.RecountLinks.home, link.RecountLinks.dashboardHome],
            style={
                "display": "flex",
                "justifyContent": "spaceBetween",
                "height": "100px",
            },
        )
        whole_page = html.Div(children=[links_div, page_content])
        return whole_page
