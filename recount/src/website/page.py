import abc

from .vue import *
from .action import *


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


class IndexPage(Index, Page):
    page_name = "index-page"


class HomePage(Home, Page):
    page_name = "home-page"


class DashboardHomePage(DashboardHomeMixin, DashboardHomeVue, Page):
    page_name = "dashboard-home-page"


class NotebookHomePage(NotebookHomeMixin, NotebookHomeVue, Page):
    page_name = "notebook-home-page"
