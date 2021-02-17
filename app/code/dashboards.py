import dash
import dash_html_components as html
import dash_core_components as dcc

import datetime


import communication_db

import wrapper_excel.paths_docs as paths_docs
TSTAuthPath = paths_docs.ThemesAndSubthemesAuthorized()

import wrapper_excel.access_docs as access_docs
AuthorizedTST = access_docs.AccessTSTAuthorized(TSTAuthPath)
authorizedTST_json = AuthorizedTST.getJson()

import wrapper_dash.prepare_dashboard as prepare_dashboard
import wrapper_dash.main_convert_df_to_graph as main_convert_df_to_graph
import wrapper_dash.convert_ld_to_graph as convert_ld_to_graph
import wrapper_dash.convert_df_to_ld as convert_df_to_ld
DataframeToListDict = convert_df_to_ld.DataframeToListOfDicts()
ListDictToGraph = convert_ld_to_graph.ListDictToGraph(authorizedTST_json)
ConvertDfToGraph = main_convert_df_to_graph.DataframeToGraph(DataframeToListDict, ListDictToGraph)



class DashboardA():
    def __init__(self):
        self.EmptyDashboard = prepare_dashboard.EmptyDashboard()
        self.app = dash.Dash()
        
        self.DateToDataframe = communication_db.DateToDataframe()
        self.ConvertDfToGraph = ConvertDfToGraph
    
    def callback(self):
        @self.app.callback(
            [dash.dependencies.Output("scatter-output", "figure"),
            dash.dependencies.Output("pie-output", "figure"),
            dash.dependencies.Output("mean-output", "figure"),
            dash.dependencies.Output("food-output", "figure")],
            [dash.dependencies.Input("input-date", 'date'),
            dash.dependencies.Input("input-radio", 'value')])
        def update_graph(selected_date_str, selected_periode):        
            dataframe = self.DateToDataframe.getDataframeFromDate(selected_date_str, selected_periode)
            list_dataframes = self.DateToDataframe.getListDataframeByWeekFromDate(selected_date_str, selected_periode)
            
            scatter_graph = self.ConvertDfToGraph.convertDataframeToGraph(dataframe, "all-scatter")
            pie_graph = self.ConvertDfToGraph.convertDataframeToGraph(dataframe, "theme-pie")
            mean_graph = self.ConvertDfToGraph.convertDataframeToGraph(list_dataframes, "mean-bar")
            food_graph = self.ConvertDfToGraph.convertDataframeToGraph(list_dataframes, "food-bar")
            
            return scatter_graph, pie_graph, mean_graph, food_graph

    
    def prepareDashboard(self):
        self.app.layout = self.EmptyDashboard.getEmptyDashboardA()
        self.callback()
            
    def run(self):
        self.app.run_server(debug=True)
        
    
    def launch(self):
        self.prepareDashboard()
        print("-#- Application Running -#-")
        self.run()
    


class DashboardV(): #Dashboard of trips
    def __init__(self):
        self.EmptyDashboard = prepare_dashboard.EmptyDashboard()
        self.app = dash.Dash()
        
        self.DateToDataframe = communication_db.DateToDataframe()
        self.ConvertDfToGraph = ConvertDfToGraph
    
    def callback(self):
        @self.app.callback(
            [dash.dependencies.Output("scatter-output", "figure"),
            dash.dependencies.Output("pie-output", "figure"),
            dash.dependencies.Output("mean-output", "figure"),
            dash.dependencies.Output("food-output", "figure")],
            [dash.dependencies.Input("input-date", 'date'),
            dash.dependencies.Input("input-radio", 'value')])
        def update_graph(selected_date_str, selected_periode):        
            start_date = convertStrToDatetime(selected_date_str)
            
            dataframe = self.DateToDataframe.getDataframeFromDate(start_date, selected_periode)
            list_dataframes = self.DateToDataframe.getListDataframeByWeekFromDate(start_date, selected_periode)
            
            scatter_graph = self.ConvertDfToGraph.convertDataframeToGraph(dataframe, "all-scatter")
            pie_graph = self.ConvertDfToGraph.convertDataframeToGraph(dataframe, "theme-pie")
            mean_graph = self.ConvertDfToGraph.convertDataframeToGraph(list_dataframes, "mean-bar")
            food_graph = self.ConvertDfToGraph.convertDataframeToGraph(list_dataframes, "food-bar")
            
            return scatter_graph, pie_graph, mean_graph, food_graph

    
    def prepareDashboard(self):
        self.app.layout = self.EmptyDashboard.getEmptyDashboardA()
        self.callback()
            
    def run(self):
        self.app.run_server(debug=True)
        
        
        
        
    def testGraph(self, graph):
        # all-scatter, theme-pie, mean-bar, food-bar
        self.app.layout = dcc.Graph(figure=graph)
        self.app.run_server(debug=True)
        
    
    



def convertStrToDatetime(my_date):
    try:
        formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S.%f")
        return formated_date
    except ValueError:
        pass
    
    try:
        formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%d")
        return formated_date
    except ValueError:
        pass
    
    raise Exception