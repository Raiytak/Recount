from dash import dcc, html
from dash.dependencies import Output, Input

from .component import RecountComponents
from .css_style import *


class DashboardHome(RecountComponents):
    def graphDataOutputCallback(self):
        return Output(self.graph_data, "data")

    def graphDataInputCallback(self):
        return Input(self.graph_data, "data")

    def defaultGraph(self, graph_id):
        graph = dcc.Graph(
            id=graph_id, config={"edits": {"axisTitleText": True, "titleText": True}},
        )
        return graph

    def dashboardHome(self):
        scatter_graph = self.defaultGraph(self.scatter_id)
        pie_chart_graph = self.defaultGraph(self.pie_chart_id)
        upper_graphs = html.Div([scatter_graph, pie_chart_graph], style=spaceAround)

        mean_bar_graph = self.defaultGraph(self.mean_bar_id)
        food_bar_graph = self.defaultGraph(self.food_bar_id)
        bottom_graphs = html.Div([mean_bar_graph, food_bar_graph], style=spaceAround)

        dashboard_div = html.Div([upper_graphs, bottom_graphs])
        return dashboard_div

    def dashboardHomeCallbacks(self):
        return [
            Output(self.scatter_id, component_property="figure"),
            Output(self.pie_chart_id, component_property="figure"),
            Output(self.mean_bar_id, component_property="figure"),
            Output(self.food_bar_id, component_property="figure"),
        ]
