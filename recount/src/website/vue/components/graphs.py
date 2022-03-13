from dash import dcc, html
from dash.dependencies import Output

from .css_style import *


class RecountGraphs:
    def __init__(self, name_vue):
        self.name_vue = name_vue

        self.scatter_type = "-scatter-graph"
        self.pie_chart_type = "-pie-chart-category"
        self.mean_bar_type = "-mean-bar"
        self.food_bar_type = "-food-bar"

        self.scatter_id = self.name_vue + self.scatter_type
        self.pie_chart_id = self.name_vue + self.pie_chart_type
        self.mean_bar_id = self.name_vue + self.mean_bar_type
        self.food_bar_id = self.name_vue + self.food_bar_type

    def defaultGraphVue(self, graph_id):
        graph = dcc.Graph(
            id=graph_id, config={"edits": {"axisTitleText": True, "titleText": True}},
        )
        return graph

    def defaultGraphCallback(self, graph_id):
        return Output(graph_id, component_property="figure")

    def dashboardHomeDiv(self):
        scatter_graph = self.defaultGraphVue(self.scatter_id)
        pie_chart_graph = self.defaultGraphVue(self.pie_chart_id)
        upper_graphs = html.Div([scatter_graph, pie_chart_graph], style=spaceAround)

        mean_bar_graph = self.defaultGraphVue(self.mean_bar_id)
        food_bar_graph = self.defaultGraphVue(self.food_bar_id)
        bottom_graphs = html.Div([mean_bar_graph, food_bar_graph], style=spaceAround)

        dashboard_div = html.Div([upper_graphs, bottom_graphs])
        return dashboard_div

    def dashboardHomeCallbacks(self):
        return {
            "scatter": self.defaultGraphCallback(self.scatter_id),
            "pie": self.defaultGraphCallback(self.pie_chart_id),
            "mean": self.defaultGraphCallback(self.mean_bar_id),
            "bar": self.defaultGraphCallback(self.food_bar_id),
        }
