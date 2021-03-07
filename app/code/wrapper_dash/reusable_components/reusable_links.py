import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, State

import wrapper_dash.reusable_components.reusable_styles as reusable_styles



class ReusableSingleLinks():
    def __init__(self):
        self.ReusableStyles = reusable_styles.ReusableStyles()

    def getLinkPageDashhome(self):
        link_page_dashhome = dcc.Link('Dashboards', href='/dashhome', className="header-link")
        return link_page_dashhome

    def getLinkPageHome(self):
        link_page_home = dcc.Link('Home', href='/home', className="header-link")
        return link_page_home

    def getLinkPageCategories(self):
        link_page_categories = dcc.Link('Categories', href='/categories', className="header-link")
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
        link_page_categories = self.getLinkPageCategories()

        links_div = html.Nav(
            children=[
                html.Button(link_page_home, className="header-button"),
                html.Button(link_page_dashhome, className="header-button"),
                html.Button(link_page_categories, className="header-button")
            ],
            style={
                "display":"flex",
                "justify-content":"space-between"}
                )
        return links_div


    def getLogoDivSite(self):
        logo = self.getImageSite()
        logo_div = html.A(
            children=logo, 
            href="/"
        )
        return logo_div

    def getHeaderSite(self):
        logo_div = self.getLogoDivSite()
        links_div = self.getLinksDiv()

        header_site = html.Div(
            children=[
                logo_div,
                links_div
            ],
            style={
                "display":"flex",
                "justify-content":"space-between"
                }
        )
        return header_site



