import pandas
from dash import dash_table, html, dcc

from src.pipeline.convert import shapeDatetimeToSimpleDate
from src.access.access_files import UserFilesAccess
from .component import RecountDefaultDivs
from .css_style import *

__all__ = ["RecountNotebook"]


class RecountNotebook(RecountDefaultDivs):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.notebook = self.name_vue + "-notebook-home"
        self.add_row_button = self.name_vue + "-add-row-button"

    def addRowButton(self):
        add_row = html.Button(id=self.add_row_button, children="Add Row")
        return html.Div([add_row])

    def notebookHome(self):
        example = UserFilesAccess.shortExample
        example_data = pandas.read_excel(example)

        # TODO: better date
        # def date_or_pass(value):
        #     return shapeDatetimeToSimpleDate(value) if pandas.notna(value) else value

        # example_data_date = example_data["Date"].apply(date_or_pass)
        import_export_reset_div = self.uploadDownloadResetDiv()
        upper_div = html.Div([html.Div(), import_export_reset_div], style=spaceBetween,)
        notebook_div = dash_table.DataTable(
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
            data=example_data.to_dict("records"),
            editable=True,
            row_deletable=True,
            export_columns="all",
            export_format="xlsx",
            export_headers="display",
        )
        return html.Div([upper_div, notebook_div])
