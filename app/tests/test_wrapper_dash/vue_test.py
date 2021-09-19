import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import wrapper_dash.vue_links_other_vues as vue_links_other_vues

import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_links as reusable_links

import wrapper_dash.reusable_components.reusable_standard_buttons as reusable_standard_buttons


class ElementsVue:
    def __init__(self, ReusableInputs, ReusableLinks, ReusableStandardButtons):
        self.ReusableInputs = ReusableInputs
        self.ReusableLinks = ReusableLinks
        self.ReusableStandardButtons = ReusableStandardButtons

    def getInputDiv(self):
        return self.ReusableInputs.getDatePeriodAndExcelDiv()

    def getOutputDiv(self):
        return html.Div()

    def getLinksDiv(self):
        return self.ReusableLinks.getRowTypeLinksDiv()


class EmptyVue:
    def __init__(self):
        self.name_vue = "test-page-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableLinks = reusable_links.ReusableLinks()
        # self.ReusableStandardButtons = reusable_standard_buttons.ReusableStandardButtons()
        self.ReusableStandardButtons = 0
        self.elementsVue = ElementsVue(
            self.ReusableInputs, self.ReusableLinks, self.ReusableStandardButtons
        )

    def getEmptyVue(self):
        elem_input_div = self.elementsVue.getInputDiv()
        elem_output_div = self.elementsVue.getOutputDiv()
        top_vue = html.Div(children=[elem_input_div, elem_output_div])

        elem_links_div = self.elementsVue.getLinksDiv()
        bottom_vue = html.Div(elem_links_div)

        all_the_vue = html.Div([top_vue, bottom_vue])
        return all_the_vue

    def getInputCallbacks(self):
        return self.ReusableInputs.getLocationCallback()


# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setCallback()

    def setCallback(self):
        @self.app.callback(
            Output("page-content-test", "children"), self.getInputCallbacks()
        )
        def display_home(pathname):
            return ""

    def setThisVue(self):
        return self.getEmptyVue()
