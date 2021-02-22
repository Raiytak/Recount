import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, State





class ReusableGraphs():
    def __init__(self, name_vue):
        self.name_vue = name_vue

        self.scatter_type = "scatter-graph-all"
        self.pie_chart_type = "pie-chart-category"
        self.mean_bar_type = "mean-bar"
        self.food_bar_type = "food-bar"


        self.scatter_id = self.name_vue+self.scatter_type
        self.pie_chart_id = self.name_vue+self.pie_chart_type
        self.mean_bar_id = self.name_vue+self.mean_bar_type
        self.food_bar_id = self.name_vue+self.food_bar_type



    def getScatterGraphDiv(self):
        scatter_graph = dcc.Graph(id=self.scatter_id)
        return scatter_graph
    def getPieChartGraphDiv(self):
        pie_chart_graph = dcc.Graph(id=self.pie_chart_id)
        return pie_chart_graph
    def getMeanBarGraphDiv(self):
        mean_bar_graph = dcc.Graph(id=self.mean_bar_id)
        return mean_bar_graph
    def getFoodBarGraphDiv(self):
        food_bar_graph = dcc.Graph(id=self.food_bar_id)
        return food_bar_graph

    def getDashboardHomeDiv(self):
        scatter_graph = self.getScatterGraphDiv()
        pie_chart_graph = self.getPieChartGraphDiv()
        upper_graphs = html.Div([scatter_graph, pie_chart_graph],
                                    style= {'display': 'flex',
                                        "justify-content":"space-around"})

        mean_bar_graph = self.getMeanBarGraphDiv()
        food_bar_graph = self.getFoodBarGraphDiv()
        bottom_graphs = html.Div([mean_bar_graph, food_bar_graph],
                                    style= {'display': 'flex',
                                        "justify-content":"space-around"})
        
        dashboard_div = html.Div([
            upper_graphs,
            bottom_graphs,
        ])
        return dashboard_div

    def getDashboardHomeTypeGraphs(self):
        list_type_divs = []
        list_type_divs.append(self.scatter_type)
        list_type_divs.append(self.pie_chart_type)
        list_type_divs.append(self.mean_bar_type)
        list_type_divs.append(self.food_bar_type)
        return list_type_divs



    def getScatterGraphCallback(self):
        return Output(component_id=self.scatter_id, component_property='figure')
    def getPieChartGraphCallback(self):
        return Output(component_id=self.pie_chart_id, component_property='figure')
    def getMeanBarGraphCallback(self):
        return Output(component_id=self.mean_bar_id, component_property='figure')
    def getFoodBarGraphCallback(self):
        return Output(component_id=self.food_bar_id, component_property='figure')

    def getlDashboardHomeCallbacks(self):
        callbacks = []
        callbacks.append(self.getScatterGraphCallback())
        callbacks.append(self.getPieChartGraphCallback())
        callbacks.append(self.getMeanBarGraphCallback())
        callbacks.append(self.getFoodBarGraphCallback())
        return callbacks
        


