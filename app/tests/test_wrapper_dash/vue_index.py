import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import wrapper_dash.vue_links_other_vues as vue_links_other_vues

import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_links as reusable_links


class ElementsVue:
    def __init__(self, ReusableInputs, ReusableLinks):
        self.ReusableInputs = ReusableInputs
        self.ReusableLinks = ReusableLinks

    def getInputDiv(self):
        return self.ReusableInputs.getDatePeriodAndExcelDiv()

    def getOutputDiv(self):
        return html.Div(id="default-page-content")

    def getLinksDiv(self):
        return self.ReusableLinks.getHeaderSite()

    def getLocationDiv(self):
        return self.ReusableInputs.getLocationDiv()


class EmptyVue:
    def __init__(self):
        self.name_vue = "index-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableLinks = reusable_links.ReusableLinks()
        self.elementsVue = ElementsVue(self.ReusableInputs, self.ReusableLinks)

    def getEmptyDefaultVue(self):
        location = self.elementsVue.getLocationDiv()
        page_content = self.elementsVue.getOutputDiv()
        default_input_div = html.Div(children=[location, page_content])
        return default_input_div

    def getEmptyVue(self):
        elem_links_div = self.elementsVue.getLinksDiv()
        all_the_vue = html.Div([elem_links_div])
        return all_the_vue


# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app
        # self.setCallback()

    # def setCallback(self):
    #     @self.app.callback(
    #         Output('page-content-home', 'children'),
    #         self.getInputCallbacks()
    #     )
    #     def display_home(pathname):
    #         return ''

    def setThisEmptyDefaultVue(self):
        return self.getEmptyDefaultVue()

    def setThisVue(self):
        return self.getEmptyVue()
