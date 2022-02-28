import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from wrapper_dash.reusable_components.reusable_inputs import ReusableInputs
from wrapper_dash.reusable_components.reusable_links import ReusableLinks


class ElementsVue:
    def __init__(self, ReusableInputs, ReusableLinks):
        self.ReusableInputs = ReusableInputs
        self.ReusableLinks = ReusableLinks

    def getOutputDiv(self):
        return html.Div(id="default-page-content")

    def getLinksDiv(self):
        return self.ReusableLinks.getNavDivSite()

    def getLocationDiv(self):
        return self.ReusableInputs.getLocationDiv()


class EmptyVue:
    def __init__(self):
        self.name_vue = "index-"
        self.ReusableInputs = ReusableInputs(self.name_vue)
        self.ReusableLinks = ReusableLinks()
        self.ElementsVue = ElementsVue(self.ReusableInputs, self.ReusableLinks)

    def getEmptyDefaultVue(self):
        location = self.ElementsVue.getLocationDiv()
        elem_links_div = self.ElementsVue.getLinksDiv()
        page_content = self.ElementsVue.getOutputDiv()
        header_site = html.Div(
            elem_links_div,
            style={"display": "flex", "justify-content": "space-between"},
        )
        default_input_div = html.Div(children=[location, header_site, page_content])
        return default_input_div

    def getEmptyVue(self):
        elem_links_div = self.ElementsVue.getLinksDiv()
        all_the_vue = html.Div(elem_links_div)
        return all_the_vue


# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app

    #     self.setCallback()

    # def setCallback(self):
    #     @self.app.callback(
    #         Output('page-content-home', 'children'),
    #         [self.getInputCallbacks()]
    #     )
    #     def reset_data(n_clicks):
    #         print("ici")
    #         print(n_clicks)
    #         raise Exception("My Exception")
    #         return ""

    def setDefaultVue(self):
        return self.getEmptyDefaultVue()

    def setThisVue(self):
        return ""
