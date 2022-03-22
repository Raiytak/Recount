from dash import dcc, html
from dash.dependencies import Output, Input

from .component import RecountComponents
from .css_style import *


class RecountNotebook(RecountComponents):
    def graphDataOutputCallback(self):
        return Output(self.graph_data, "data")

    def getDashNotebookDivFromDataframe(self, dataframe):
        columns_name = self.getColumnsNameFromConfig()
        notebook_excel_div = dash_table.DataTable(
            id=self.notebook_name,
            columns=[
                {
                    "name": columns_name[i],
                    "id": i,
                    "editable": False,
                    "hideable": True,
                    "renamable": True,
                }
                if i == "ID"
                else {
                    "name": columns_name[i],
                    "id": i,
                    "type": "numeric",
                    "hideable": True,
                    "renamable": True,
                }
                if (i == "Expense Euros" or i == "Expense Dollars")
                else {
                    "name": columns_name[i],
                    "id": i,
                    "type": "text",
                    "hideable": True,
                    "renamable": True,
                }
                if (i == "Description" or i == "Category" or i == "Trip")
                else {
                    "name": columns_name[i],
                    "id": i,
                    "type": "datetime",
                    "hideable": True,
                    "renamable": True,
                }
                if i == "Date"
                else {
                    "name": columns_name[i],
                    "id": i,
                    "hideable": True,
                    "renamable": True,
                }
                for i in dataframe.columns
            ],
            data=self.getNotebookData(),
            editable=True,
            row_deletable=True,
            export_columns="all",
            export_format="xlsx",
            export_headers="display",
        )
        return notebook_excel_div
