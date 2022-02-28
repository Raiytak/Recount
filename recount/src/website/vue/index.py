import dash_html_components as html
import dash_core_components as dcc

from .abstract_vue import AbstractVue
from .components import links

from recount_tools import classproperty


class Index(AbstractVue):
    @classproperty
    def vue(cls):
        # represents the browser address bar and doesn't render anything
        url = dcc.Location(id="url", refresh=False)
        page_content = html.Div(id="page-content")
        links_div = html.Nav(
            children=[url, links.Links.home, links.Links.dashboardHome],
            style={
                "display": "flex",
                "justify-content": "space-between",
                "height": "100px",
            },
        )
        whole_page = html.Div(children=[links_div, page_content])
        return whole_page
