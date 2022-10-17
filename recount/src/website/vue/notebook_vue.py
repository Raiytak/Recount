from dash import html, dcc

from .abstract_vue import AbstractVue

from .components import *
from .components.css_style import *

__all__ = ["NotebookHomeVue"]


class NotebookHomeVue(AbstractVue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notebook_home = RecountNotebook(self.page_name)

    @property
    def vue(self):
        upper_div = html.Div(
            [html.Div(), self.notebook_home.dashboardInputDiv()], style=spaceBetween
        )
        notebook_home = self.notebook_home.notebookHome()
        add_row = self.notebook_home.addRowButton()

        return html.Div([upper_div, notebook_home, add_row])
