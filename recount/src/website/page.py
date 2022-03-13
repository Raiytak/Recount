import abc

from .vue import index, home, dashboard
from .action.dashboard import DashboardMixin

# TODO: def __init__ here, define name vue, call super.
# The vue name should be transfered to both action and vue!


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


class DashboardHomePage(DashboardMixin, dashboard.DashboardHome, Page):
    page_name = "dashboard-home-page"
