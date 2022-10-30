from dash import dcc, html
from dash.dependencies import Output, Input

from .component import RecountDefaultDivs, DefaultButtons
from .css_style import *

__all__ = ["DashboardHome"]


class DashboardHome(RecountDefaultDivs):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.update_graph_button = self.name_vue + "-update-graph-button"
        self.update_data_button = self.name_vue + "-update-data-button"

        self.dashboard = self.name_vue + "-dashboard"
        self.scatter_id = self.name_vue + "-scatter-graph"
        self.pie_chart_id = self.name_vue + "-pie-chart-category"
        self.mean_bar_id = self.name_vue + "-mean-bar"
        self.food_bar_id = self.name_vue + "-food-bar"

    def graphDataOutputCallback(self):
        return Output(self.graph_data, "data")

    def graphDataInputCallback(self):
        return Input(self.graph_data, "data")

    def defaultGraph(self, graph_id):
        graph = dcc.Graph(
            id=graph_id, config={"edits": {"axisTitleText": True, "titleText": True}},
        )
        return graph

    def dashboardDiv(self):
        scatter_graph = self.defaultGraph(self.scatter_id)
        pie_chart_graph = self.defaultGraph(self.pie_chart_id)
        upper_graphs = html.Div([scatter_graph, pie_chart_graph], style=spaceAround)

        mean_bar_graph = self.defaultGraph(self.mean_bar_id)
        food_bar_graph = self.defaultGraph(self.food_bar_id)
        bottom_graphs = html.Div([mean_bar_graph, food_bar_graph], style=spaceAround)

        dashboard_div = html.Div(
            id=self.dashboard, children=[upper_graphs, bottom_graphs]
        )
        return dashboard_div

    def dashboardCallbacks(self):
        return [
            Output(self.scatter_id, component_property="figure"),
            Output(self.pie_chart_id, component_property="figure"),
            Output(self.mean_bar_id, component_property="figure"),
            Output(self.food_bar_id, component_property="figure"),
        ]

    def dashboardInputDiv(self):
        date_period_div = self.datePeriodDiv()
        refresh_graph_button = html.Button(
            id=self.update_graph_button, children="Refresh Graph", n_clicks=0,
        )
        refresh_data_button = html.Button(
            id=self.update_data_button, children="Refresh Data", n_clicks=0,
        )

        import_export_reset_div = DefaultButtons.uploadDownloadResetDiv()
        refresh_div = html.Div(
            children=[refresh_graph_button, refresh_data_button], style=flexColumn
        )
        buttons_div = html.Div(
            children=[refresh_div, import_export_reset_div], style=flex
        )
        all_divs = html.Div(children=[date_period_div, buttons_div], style=spaceBetween)
        return all_divs
