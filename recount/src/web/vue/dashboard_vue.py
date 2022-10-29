from dash import html, dcc

from .abstract_vue import AbstractVue

from .components.css_style import *
from .components import *

__all__ = ["DashboardHomeVue"]


class DashboardHomeVue(AbstractVue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dashboard_home = DashboardHome(self.page_name)

    @property
    def vue(self):
        loading_div = self.dashboard_home.loadingDiv()
        upper_div = self.dashboard_home.dashboardInputDiv()
        dashboard_div = self.dashboard_home.dashboardDiv()
        dashboard = html.Div([upper_div, loading_div, dashboard_div])

        return dashboard
