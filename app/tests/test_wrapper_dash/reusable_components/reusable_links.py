import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, State

import wrapper_dash.reusable_components.reusable_styles as reusable_styles


class ReusableSingleLinks:
    def __init__(self):
        self.ReusableStyles = reusable_styles.ReusableStyles()

    def getLinkPageHome(self):
        link_page_home = html.Button("Home", className="header-button")
        return link_page_home

    def getLinkPageDashhome(self):
        link_page_dashhome = html.Button("Dashboard", className="header-button")
        return link_page_dashhome

    def getLinkPageNotebook(self):
        link_page_notebook = html.Button("Notebook", className="header-button")
        return link_page_notebook

    def getLinkPageCategories(self):
        link_page_categories = html.Button("Categories", className="header-button")
        return link_page_categories

    def getImageSite(self):
        logo_site = html.Img(
            src="/assets/doit.gif",
            # height=100,
        )
        return logo_site


class ReusableLinks(ReusableSingleLinks):
    def __init__(self):
        super().__init__()

    def getLinksDiv(self):
        link_page_home = self.getLinkPageHome()
        link_page_dashhome = self.getLinkPageDashhome()
        # link_page_notebook = self.getLinkPageNotebook()
        # link_page_categories = self.getLinkPageCategories()

        links_div = html.Nav(
            children=[
                dcc.Link(link_page_home, className="header-link", href="/home"),
                dcc.Link(link_page_dashhome, className="header-link", href="/dashhome"),
                # dcc.Link(link_page_notebook, className="header-link", href='/excel'),
                # dcc.Link(link_page_categories, className="header-link", href='/categories')
            ],
            style={
                "display": "flex",
                "justify-content": "space-between",
                "height": "100px",
            },
        )
        return links_div

    def getLogoDivSite(self):
        logo = self.getImageSite()
        logo_div = html.A(children=logo, href="/assets/notme.gif")
        return logo_div

    def getHeaderSite(self):
        links_div = self.getLinksDiv()

        header_site = html.Header(children=[links_div], style={"display": "flex"})
        return header_site
