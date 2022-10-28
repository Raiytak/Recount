import abc

from .vue import *
from .action import *

__all__ = [
    "IndexPage",
    "HomePage",
    "DashboardHomePage",
    "CategoryHomePage",
    # "NotebookHomePage",
]


class Page:
    def __init__(self, page_name=None, *args, **kwargs):
        if page_name:
            self.page_name
        super().__init__(*args, **kwargs)

    @abc.abstractproperty
    def vue(self):
        """Returns the vue of the page"""

    @abc.abstractproperty
    def page_name(self):
        """Name of the vue"""


class IndexPage(IndexVue, Page):
    page_name = "index-page"


class HomePage(HomeVue, Page):
    page_name = "home-page"


class CategoryHomePage(CategoryHomeMixin, CategoryHomeVue, Page):
    page_name = "category-home-page"


class DashboardHomePage(DashboardHomeMixin, DashboardHomeVue, Page):
    page_name = "dashboard-home-page"


# class NotebookHomePage(NotebookHomeMixin, NotebookHomeVue, Page):
#     page_name = "notebook-home-page"
