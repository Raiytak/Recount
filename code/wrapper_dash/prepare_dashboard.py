import dash
import dash_html_components as html
import dash_core_components as dcc

import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta






class GraphInit():
    def getInputDivA(self):
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
            date = dt.now()-relativedelta(months=4),
            display_format="D/M/Y"
        )
        input_div = html.Div(children=[date_input,
                                       periode_input])
        return input_div

    def getEmptyGraphA(self, graph_type):
        if graph_type=="scatter":
            return dcc.Graph(id="scatter-output")
        if graph_type=="pie":
            return dcc.Graph(id="pie-output")
        if graph_type=="mean":
            return dcc.Graph(id="mean-output")
        if graph_type=="food":
            return dcc.Graph(id="food-output")
        

class EmptyDashboard():
    def __init__(self):
        self.graphInit = GraphInit()
        
    def getEmptyDashboardA(self):
        input_div = self.graphInit.getInputDivA()
        
        scatter_graph = self.graphInit.getEmptyGraphA("scatter")
        pie_graph = self.graphInit.getEmptyGraphA("pie")
        upper_graphs = html.Div([scatter_graph, pie_graph],
                                    style= {'display': 'flex'})
        upper_dashboard = html.Div([input_div, upper_graphs],
                                    style= {'display': 'block'})
        
        mean_graph = self.graphInit.getEmptyGraphA("mean")
        food_graph = self.graphInit.getEmptyGraphA("food")
        bottom_dashboard = html.Div([mean_graph, food_graph],
                                    style= {'display': 'flex'})
        
        dashboard = html.Div([
            upper_dashboard,
            bottom_dashboard,
        ])
        
        return dashboard