import logging
from dash import callback, html, dcc, Input, Output, State

from .tools import *

# from pipeline.pipeline import UserDataPipeline, UserGraphPipeline

from .abstract_mixin import AbstractAction

from src.web.vue.components.css_style import *
from .graphs import *

__all__ = ["CategoryMixin"]


class CategoryMixin(AbstractAction):
    CATEGORY = "category-"
    DEPTH = "depth-"
    BUTTON = "button"
    MAX_DEPTH = 4

    def setCallbacks(self):
        return
        # TODO: should be called at beginning
        @callback(*self.osi_cancel_button_pressed)
        def cancel_button_pressed(*args):
            return self.cancel_button_pressed(*args)

    @property
    def osi_cancel_button_pressed(self):
        return (
            Output(self.category_home.layer + "1", "children"),
            Output(self.category_home.loading_div, "children"),
            Input(self.category_home.cancel_modifications_button, "n_clicks"),
            # State(self.category_home.category_diplay_div, "children"),
        )

    @staticmethod
    def cancel_button_pressed(cancel_n_clicks):
        username = getUsername()
        user_data = UserDataPipeline(username)
        categories = user_data.user_files.categories
        categories_div = CategoryMixin.categoryDivOfDepth(categories, depth=0)
        return categories_div, None

    @staticmethod
    def categoryDivOfDepth(categories: dict, depth: int):
        main_layer = []
        for category, subcategories in sorted(categories.items()):
            if subcategories:
                sub_layer = CategoryMixin.categoryDivOfDepth(subcategories, depth + 1)
                category_layer = CategoryMixin.createDivForCategory(
                    category, sub_layer, depth
                )
                main_layer.append(category_layer)
            else:
                button = CategoryMixin.createButtonForCategory(category, depth)
                main_layer.append(button)

        return html.Div(main_layer)

    def createDivForCategory(name: str, children: list, depth: int):
        category = CategoryMixin.createButtonForCategory(name, depth)
        sub_categories = html.Div(
            children,
            className=CategoryMixin.CATEGORY + " " + CategoryMixin.DEPTH + str(depth),
        )
        return html.Div([category, sub_categories], style=flex)

    def createButtonForCategory(children: str, depth: int):
        return html.Button(
            children,
            className=CategoryMixin.CATEGORY
            + " "
            + CategoryMixin.DEPTH
            + str(depth)
            + " "
            + CategoryMixin.BUTTON,
        )
