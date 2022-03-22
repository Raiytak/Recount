from dash import html

from .abstract_vue import AbstractVue

from .components import *


class DashboardHome(AbstractVue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.recount_graphs = RecountGraphs(self.page_name)

    @property
    def vue(self):
        conf_dial = self.recount_graphs.confirmDialogueDiv(
            message="Are you sure you want to reset your data?"
        )

        upper_div = self.recount_graphs.dashboardInputDiv()
        dashboard_div = self.recount_graphs.dashboardHome()
        dashboard = html.Div([upper_div, dashboard_div])

        test_div = self.recount_graphs.testDiv()

        total_vue = html.Div([test_div, dashboard, conf_dial])

        return total_vue
