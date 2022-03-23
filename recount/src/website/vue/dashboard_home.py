from dash import html

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
        upper_div = self.dashboard_home.dashboardInputDiv()
        dashboard_div = self.dashboard_home.dashboardHome()
        dashboard = html.Div([upper_div, dashboard_div])

        test_div = self.dashboard_home.testDiv()

        total_vue = html.Div([test_div, dashboard])

        return total_vue
