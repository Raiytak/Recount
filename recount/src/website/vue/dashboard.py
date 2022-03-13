from dash import html

from .abstract_vue import AbstractVue

from .components import *


class DashboardHome(AbstractVue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.recount_inputs = RecountInputs(self.page_name)
        self.recount_outputs = RecountOutputs(self.page_name)
        self.recount_graphs = RecountGraphs(self.page_name)

    @property
    def vue(self):
        conf_dial = self.recount_outputs.confirmDialogue()

        upper_div = self.recount_inputs.dashboardInputDiv()
        dashboard_div = self.recount_graphs.dashboardHomeDiv()
        dashboard = html.Div([upper_div, dashboard_div])

        hidden_vue = self.recount_outputs.hiddenDiv()

        total_vue = html.Div([dashboard, hidden_vue, conf_dial])

        return total_vue

    @property
    def output_callbacks(self):
        return self.recount_graphs.dashboardHomeCallbacks()

    @property
    def input_callbacks(self):
        rec_in = self.recount_inputs
        return {
            "date": rec_in.dateCallback(),
            "period": rec_in.periodCallback(),
            "import": rec_in.importExcelCallback(),
            "reset": rec_in.resetUserDataCallback(),
        }
