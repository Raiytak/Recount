import abc

from .vue import dashboard_home, index, home
from .action.dashboard_home import DashboardHomeMixin


class Page:
    def __init__(self, app, page_name=None, *args, **kwargs):
        self.app = app
        if page_name:
            self.page_name
        super().__init__(*args, **kwargs)

    @abc.abstractproperty
    def vue(self):
        """Returns the vue of the page"""

    @abc.abstractproperty
    def page_name(self):
        """Name of the vue"""


class IndexPage(index.Index, Page):
    page_name = "index-page"


class HomePage(home.Home, Page):
    page_name = "home-page"


class DashboardHomePage(DashboardHomeMixin, dashboard_home.DashboardHomeVue, Page):
    page_name = "dashboard-home-page"
