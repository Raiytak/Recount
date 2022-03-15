from dash import html

from .abstract_vue import AbstractVue

from .components import *


class DashboardHome(AbstractVue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.recount_inputs = RecountInputs(self.page_name)
        self.recount_outputs = RecountOutputs(self.page_name)
        self.recount_graphs = RecountGraphs(self.page_name)

        self.reset_dial = "reset-data"

    @property
    def vue(self):
        conf_dial = self.recount_outputs.confirmDialogueDiv(
            self.reset_dial, message="Are you sure you want to reset your data?"
        )

        upper_div = self.recount_inputs.dashboardInputDiv()
        dashboard_div = self.recount_graphs.dashboardHomeDiv()
        dashboard = html.Div([upper_div, dashboard_div])

        total_vue = html.Div([dashboard, conf_dial])

        return total_vue
