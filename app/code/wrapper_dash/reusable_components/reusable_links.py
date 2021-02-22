import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, State



class ReusableSingleLinks():
    def __init__(self):
        pass

    def getLinkPageDashhome(self):
        link_page_dashhome = dcc.Link('Go to Page Dashboard Home', href='/dashhome')
        return link_page_dashhome

    def getLinkPageHome(self):
        link_page_home = dcc.Link('Go to Page Home', href='/home')
        return link_page_home

    def getLinkPageCategories(self):
        link_page_categories = dcc.Link('Go to Page Categories', href='/categories')
        return link_page_categories





class ReusableLinks(ReusableSingleLinks):
    def __init__(self):
        super().__init__()

    def getRowTypeLinksDiv(self):
        link_page_home = self.getLinkPageHome()
        link_page_dashhome = self.getLinkPageDashhome()
        link_page_categories = self.getLinkPageCategories()

        links_div = html.Div(children=[
            link_page_home,
            link_page_dashhome,
            link_page_categories
            ],
            style={
                "display":"flex",
                "justify-content":"space-between"}
                )
        return links_div



