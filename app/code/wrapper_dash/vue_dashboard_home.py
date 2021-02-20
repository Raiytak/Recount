import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import datetime



class ElementsVue():
    def getInputDiv(self):
        periode_input = dcc.RadioItems(
            id="input-radio",
            options=[
                {"label":"Semaine", "value":"week"},
                {"label":"Mois", "value":"month"},
                {"label":"Trimestre", "value":"semestre"}
            ],
            value='month'
        )
        date_input = dcc.DatePickerSingle(
            id="input-date",
            date = datetime.datetime(year=2019,month=9,day=1),
            display_format="D/M/Y"
        )

        excel_input = dcc.Upload(
            id='upload-data',
            children=html.Div('Import csv File'),
            multiple=False
        )
        excel_input_div = html.Button(excel_input)

        date_input_div = html.Div(  children=[date_input, periode_input],
                                    style={
                                        "display":"flex",
                                        "justify-content":"space-between"})

        input_div = html.Div(   children=[date_input_div,excel_input_div],
                                style={
                                        "display":"flex",
                                        "justify-content":"space-between"})
        return input_div

    def getEmptyGraph(self, graph_type):
        if graph_type=="scatter":
            return dcc.Graph(id="scatter-output")
        if graph_type=="pie":
            return dcc.Graph(id="pie-output")
        if graph_type=="mean":
            return dcc.Graph(id="mean-output")
        if graph_type=="food":
            return dcc.Graph(id="food-output")
        



class EmptyVue():
    def __init__(self):
        self.elementsVue = ElementsVue()
        
    def getEmptyVue(self):
        input_div = self.elementsVue.getInputDiv()
        
        scatter_graph = self.elementsVue.getEmptyGraph("scatter")
        pie_graph = self.elementsVue.getEmptyGraph("pie")
        upper_graphs = html.Div([scatter_graph, pie_graph],
                                    style= {'display': 'flex',
                                        "justify-content":"space-around"})
        upper_dashboard = html.Div([input_div, upper_graphs],
                                    style= {'display': 'block',
                                        "justify-content":"space-around"})
        
        mean_graph = self.elementsVue.getEmptyGraph("mean")
        food_graph = self.elementsVue.getEmptyGraph("food")
        bottom_dashboard = html.Div([mean_graph, food_graph],
                                    style= {'display': 'flex',
                                        "justify-content":"space-around"})
        
        dashboard = html.Div([
            upper_dashboard,
            bottom_dashboard,
        ])
        
        return dashboard





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
            [Output("scatter-output", "figure"),
            Output("pie-output", "figure"),
            Output("mean-output", "figure"),
            Output("food-output", "figure")],
            [Input("input-date", 'date'),
            Input("input-radio", 'value'),
            Input('upload-data', 'contents')])
        def update_graph(selected_date_str, selected_periode, imported_file):     
             
            self.FileSaver.saveFile(imported_file)
            
            dataframe = self.DateToDataframe.getDataframeFromDate(selected_date_str, selected_periode)
            list_dataframes = self.DateToDataframe.getListDataframeByWeekFromDate(selected_date_str, selected_periode)


            scatter_graph = self.ConvertDfToGraph.convertDataframeToGraph(dataframe, "all-scatter")
            pie_graph = self.ConvertDfToGraph.convertDataframeToGraph(dataframe, "theme-pie")
            mean_graph = self.ConvertDfToGraph.convertDataframeToGraph(list_dataframes, "mean-bar")
            food_graph = self.ConvertDfToGraph.convertDataframeToGraph(list_dataframes, "food-bar")
            
            return scatter_graph, pie_graph, mean_graph, food_graph

    def setThisVue(self):
        return self.getEmptyVue()


    
