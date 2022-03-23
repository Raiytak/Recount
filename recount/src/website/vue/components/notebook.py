from tkinter.tix import DisplayStyle
import pandas
from dash import dash_table, html, dcc

from src.pipeline.convert import shapeDatetimeToSimpleDate
from src.access.access_files import UserFilesAccess
from .component import RecountDefaultDivs, DefaultButtons
from .css_style import *

__all__ = ["RecountNotebook"]


class RecountNotebook(RecountDefaultDivs):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.update_notebook_button = self.name_vue + "-update-notebook-button"
        self.notebook = self.name_vue + "-notebook"
        self.notebook_div = self.name_vue + "-notebook-div"
        self.add_row_button = self.name_vue + "-add-row-button"

    def addRowButton(self):
        add_row = html.Button(id=self.add_row_button, children="Add Row")
        return html.Div([add_row])

    def notebookHome(self):
        # TODO: better first call
        example = UserFilesAccess.shortExample
        example_data = pandas.read_excel(example)

        notebook = dash_table.DataTable(
            id=self.notebook,
            columns=[
                {
                    "name": column,
                    "id": column,
                    "editable": False,
                    "hideable": True,
                    "renamable": True,
                }
                if column == "ID"
                else {
                    "name": column,
                    "id": column,
                    "type": "numeric",
                    "hideable": True,
                    "renamable": True,
                }
                if (column == "Amount" or column == "Reimbursement")
                else {
                    "name": column,
                    "id": column,
                    "type": "datetime",
                    "hideable": True,
                    "renamable": True,
                }
                if column == "Date"
                else {
                    "name": column,
                    "id": column,
                    "hideable": True,
                    "renamable": True,
                }
                for column in example_data.columns
            ],
            editable=True,
            row_deletable=True,
            export_columns="all",
            export_format="xlsx",
            export_headers="display",
        )
        notebook_div = html.Div(
            id=self.notebook_div, children=notebook, style={"display": "none"},
        )
        return notebook_div

    def dashboardInputDiv(self):
        refresh_data_button = html.Button(
            id=self.update_notebook_button, children="Refresh Notebook", n_clicks=0,
        )

        import_export_reset_div = DefaultButtons.uploadDownloadResetDiv()
        refresh_div = html.Div(children=[refresh_data_button], style=flexColumn)
        buttons_div = html.Div(
            children=[refresh_div, import_export_reset_div], style=flex
        )
        return buttons_div
