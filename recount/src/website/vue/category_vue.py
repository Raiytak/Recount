from dash import dcc, html

from .abstract_vue import AbstractVue

from .components.css_style import *
from .components import *

__all__ = ["CategoryHomeVue"]


class CategoryHomeVue(AbstractVue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.category_home = CategoryHome(self.page_name)

    @property
    def vue(self):
        loading_div = self.category_home.loadingDiv()
        apply_button = html.Button(
            id=self.category_home.apply_modifications_button,
            children="Apply Modifications",
            n_clicks=0,
        )
        cancel_button = html.Button(
            id=self.category_home.cancel_modifications_button,
            children="Cancel Modifications",
            n_clicks=0,
        )
        buttons_div = html.Div([apply_button, cancel_button], style=flexColumn)
        category_display = html.Div(
            id=self.category_home.category_diplay_div,
            children=[
                html.Div(id=self.category_home.layer + x, className="category-layer")
                for x in range(5)
            ],
        )
        return html.Div(
            [loading_div, html.Div([category_display, buttons_div], style=spaceBetween)]
        )
