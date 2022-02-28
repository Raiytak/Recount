import abc

from .vue import home, index


class Page:
    @abc.abstractproperty
    def vue(self):
        """Returns the vue of the page"""


class IndexPage(index.Index, Page):
    pass


class HomePage(home.Home, Page):
    pass
