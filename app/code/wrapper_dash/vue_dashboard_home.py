import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from wrapper_dash.reusable_components.reusable_inputs import ReusableInputs
from wrapper_dash.reusable_components.reusable_graphs import ReusableGraphs
from wrapper_dash.reusable_components.reusable_links import ReusableLinks

import wrapper_dash.facilitator_dash.user_identification as user_identification

import update_data


class ElementsVue:
    def __init__(self, ReusableInputs, ReusableGraphs):
        self.ReusableInputs = ReusableInputs
        self.ReusableGraphs = ReusableGraphs

    def getInputDiv(self):
        return self.ReusableInputs.getDatePeriodAndExcelDiv()

    def getInputCallbacks(self):
        return self.ReusableInputs.getDatePeriodAndExcelCallbacks()

    def getGraphDiv(self):
        return self.ReusableGraphs.getDashboardHomeDiv()

    def getGraphCallbacks(self):
        return self.ReusableGraphs.getlDashboardHomeCallbacks()

    def getOutputTypeDivs(self):
        return self.ReusableGraphs.getDashboardHomeTypeGraphs()


class EmptyVue:
    def __init__(self):
        self.name_vue = "dashboard-home-"
        self.ReusableInputs = ReusableInputs(self.name_vue)
        self.ReusableGraphs = ReusableGraphs(self.name_vue)
        self.ReusableLinks = ReusableLinks()
        self.ElementsVue = ElementsVue(self.ReusableInputs, self.ReusableGraphs)

    def getEmptyVue(self):
        header_div = self.ReusableLinks.getHeaderSite()

        input_div = self.ElementsVue.getInputDiv()
        dashboard_div = self.ElementsVue.getGraphDiv()

        dashboard = html.Div([input_div, dashboard_div])

        total_vue = html.Div([header_div, dashboard])

        return total_vue

    def getInputCallbacks(self):
        return self.ElementsVue.getInputCallbacks()

    def getOutputCallbacks(self):
        return self.ElementsVue.getGraphCallbacks()

    def getOutputTypesDiv(self):
        return self.ElementsVue.getOutputTypeDivs()


# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, DateToDataframe, ConvertDfToGraph, ImportExcelFileSaver):
        super().__init__()
        self.app = app
        self.DateToDataframe = DateToDataframe
        self.ConvertDfToGraph = ConvertDfToGraph
        self.ImportExcelFileSaver = ImportExcelFileSaver

        self.setCallback()

    def setCallback(self):
        @self.app.callback(self.getOutputCallbacks(), self.getInputCallbacks())
        def update_graph(selected_date_str, selected_periode, imported_excel):
            # Processing the actions received form the user
            username = user_identification.getUsername()

            self.ImportExcelFileSaver.saveImportedFile(username, imported_excel)

            dataframe = self.DateToDataframe.getDataframeFromDate(
                username, selected_date_str, selected_periode
            )
            list_dataframes = self.DateToDataframe.getListDataframeByWeekFromDate(
                username, selected_date_str, selected_periode
            )

            list_types_of_divs = self.getOutputTypesDiv()

            scatter_graph = self.ConvertDfToGraph.convertDataframeToGraph(
                dataframe, list_types_of_divs[0]
            )
            pie_graph = self.ConvertDfToGraph.convertDataframeToGraph(
                dataframe, list_types_of_divs[1]
            )
            mean_graph = self.ConvertDfToGraph.convertDataframeToGraph(
                list_dataframes, list_types_of_divs[2]
            )
            food_graph = self.ConvertDfToGraph.convertDataframeToGraph(
                list_dataframes, list_types_of_divs[3]
            )

            return scatter_graph, pie_graph, mean_graph, food_graph

    def setThisVue(self):
        return self.getEmptyVue()
