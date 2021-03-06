import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import datetime

import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_graphs as reusable_graphs



class ElementsVue():
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




class EmptyVue():
    def __init__(self):
        self.name_vue = "dashboard-home-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableGraphs = reusable_graphs.ReusableGraphs(self.name_vue)
        self.ElementsVue = ElementsVue(self.ReusableInputs, self.ReusableGraphs)
        
    def getEmptyVue(self):
        input_div = self.ElementsVue.getInputDiv()
        dashboard_div = self.ElementsVue.getGraphDiv()
        
        dashboard = html.Div([
            input_div,
            dashboard_div,
        ])
        
        return dashboard


    def getInputCallbacks(self):
        return self.ElementsVue.getInputCallbacks()
    def getOutputCallbacks(self):
        return self.ElementsVue.getGraphCallbacks()
        

    def getOutputTypesDiv(self):
        return self.ElementsVue.getOutputTypeDivs()
         






# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, DateToDataframe, ConvertDfToGraph, FileSaver):
        super().__init__()
        self.app = app
        self.DateToDataframe = DateToDataframe
        self.ConvertDfToGraph = ConvertDfToGraph
        self.FileSaver = FileSaver
        
        self.setCallback()
    
    def setCallback(self):
        @self.app.callback(
            self.getOutputCallbacks(),
            self.getInputCallbacks()
            )
        def update_graph(selected_date_str, selected_periode, imported_excel):     
            import flask
            print(flask.request.cookies.get('username'))
            # Processing the actions received form the user
            self.FileSaver.saveImportedFile(imported_excel)
            dataframe = self.DateToDataframe.getDataframeFromDate(selected_date_str, selected_periode)
            list_dataframes = self.DateToDataframe.getListDataframeByWeekFromDate(selected_date_str, selected_periode)


            list_types_of_divs = self.getOutputTypesDiv()

            scatter_graph = self.ConvertDfToGraph.convertDataframeToGraph(dataframe, list_types_of_divs[0])
            pie_graph = self.ConvertDfToGraph.convertDataframeToGraph(dataframe, list_types_of_divs[1])
            mean_graph = self.ConvertDfToGraph.convertDataframeToGraph(list_dataframes, list_types_of_divs[2])
            food_graph = self.ConvertDfToGraph.convertDataframeToGraph(list_dataframes, list_types_of_divs[3])
            
            return scatter_graph, pie_graph, mean_graph, food_graph

    def setThisVue(self):
        return self.getEmptyVue()


    
