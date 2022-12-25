from dash import dcc, html
from dash.dependencies import Output, Input

from .default import RecountDefaultDivs, DefaultButtons
from .css_style import *

__all__ = ["CategoryHome"]


class CategoryHome(RecountDefaultDivs):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.apply_modifications_button = self.name_vue + "-apply-modifications-button"
        self.cancel_modifications_button = (
            self.name_vue + "-cancel-modifications-button"
        )
        self.category_diplay_div = self.name_vue + "-category-display-div"
        self.layer = self.name_vue + "-layer-"
