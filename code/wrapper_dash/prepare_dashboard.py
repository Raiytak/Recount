import dash
import dash_html_components as html
import dash_core_components as dcc

import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta



class DashboardA():
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
            date = datetime.datetime(year=2019,month=9,day=1),
            display_format="D/M/Y"
        )

        excel_input = dcc.Upload(
            id='upload-data',
            children=html.Div('Import csv File'),
            multiple=False
        )

        excel_input_div = html.Button(excel_input)

        date_input_div = html.Div(children=[date_input, periode_input])

        input_div = html.Div(children=[date_input_div,excel_input_div])
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
        self.graphInitA = DashboardA()
        
    def getEmptyDashboardA(self):
        input_div = self.graphInitA.getInputDivA()
        
        scatter_graph = self.graphInitA.getEmptyGraphA("scatter")
        pie_graph = self.graphInitA.getEmptyGraphA("pie")
        upper_graphs = html.Div([scatter_graph, pie_graph],
                                    style= {'display': 'flex'})
        upper_dashboard = html.Div([input_div, upper_graphs],
                                    style= {'display': 'block'})
        
        mean_graph = self.graphInitA.getEmptyGraphA("mean")
        food_graph = self.graphInitA.getEmptyGraphA("food")
        bottom_dashboard = html.Div([mean_graph, food_graph],
                                    style= {'display': 'flex'})
        
        dashboard = html.Div([
            upper_dashboard,
            bottom_dashboard,
        ])
        
        return dashboard