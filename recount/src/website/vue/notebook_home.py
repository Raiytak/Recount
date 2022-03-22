from dash import html

from .abstract_vue import AbstractVue

from .components import *

__all__ = ["NotebookHomeVue"]


class NotebookHomeVue(AbstractVue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notebook_home = RecountNotebook(self.page_name)

    @property
    def vue(self):
        notebook_home = self.notebook_home.notebookHome()
        add_row = self.notebook_home.addRowButton()

        return html.Div([notebook_home, add_row])
