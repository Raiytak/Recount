import datetime
from dash import html, dcc

from .css_style import *


class RecountComponents:
    def __init__(self, name_vue):
        self.name_vue = name_vue

        self.location_id = name_vue + "-default-url"
        self.test = "test"

        # INPUT
        self.date_div_period_id = name_vue + "-input-radio"
        self.date_div_date_id = name_vue + "-input-date"

        self.import_excel = name_vue + "-import-excel"
        self.export_excel = name_vue + "-export-excel"

        self.add_div_div = name_vue + "-add-div"
        self.remove_div_div = name_vue + "-remove-div"

        # OUTPUT
        self.h1_div_div = name_vue + "-h1-div"
        self.h2_div_div = name_vue + "-h2-div"
        self.h3_div_div = name_vue + "-h3-div"
        self.h4_div_div = name_vue + "-h4-div"
        self.hidden_div = name_vue + "-hidden-div"
        self.conf_dial = name_vue + "-confirm-dialog"

        # BUTTON
        self.reset_button = name_vue + "-reset-button"
        self.submit_id = name_vue + "-submit-button"
        self.update_data_button = name_vue + "-update-data-button"
        self.update_graph_button = name_vue + "-update-graph-button"
        self.export_excel_button = name_vue + "-export-excel-button"

        self.edit_buttons_id = name_vue + "-edit-buttons-div"

        # GRAPH
        self.scatter_id = name_vue + "-scatter-graph"
        self.pie_chart_id = name_vue + "-pie-chart-category"
        self.mean_bar_id = name_vue + "-mean-bar"
        self.food_bar_id = name_vue + "-food-bar"

    def dashboardInputDiv(self):
        date_period_div = self.datePeriodDiv()
        refresh_graph_button = self.buttonDiv(self.update_graph_button, "Refresh Graph")
        refresh_data_button = self.buttonDiv(self.update_data_button, "Refresh Data")
        reset_button = self.buttonDiv(self.reset_button, "Reset My Data")
        import_excel = self.importExcelButton()
        export_excel = self.exportExcelButton()

        import_export_div = html.Div(
            children=[import_excel, export_excel], style=flexColumn
        )
        refresh_reset_div = html.Div(
            children=[refresh_graph_button, refresh_data_button, reset_button],
            style=flexColumn,
        )
        buttons_div = html.Div(
            children=[refresh_reset_div, import_export_div], style=flex
        )
        all_divs = html.Div(children=[date_period_div, buttons_div], style=spaceBetween)
        return all_divs

    def datePeriodDiv(self):
        period_input = self.periodDiv()
        date_input = self.dateDiv()
        date_input_div = html.Div(
            children=[date_input, period_input], style=spaceBetween
        )
        return date_input_div

    def periodDiv(self):
        period_input = dcc.RadioItems(
            id=self.date_div_period_id,
            options=[
                {"label": "Week", "value": "week"},
                {"label": "Month", "value": "month"},
                {"label": "Quarter", "value": "semestre"},
                {"label": "Annual", "value": "annual"},
            ],
            value="month",
            style={"fontSize": "medium"},
        )
        return period_input

    def dateDiv(self):
        date_input = dcc.DatePickerSingle(
            id=self.date_div_date_id,
            date=datetime.date(
                year=2019, month=9, day=1
            ),  # TODO: start at begining of user's data date
            # date = datetime.datetime.today()-relativedelta(months=5),
            display_format="D/M/Y",
        )
        return date_input

    def importExcelButton(self):
        excel_input = dcc.Upload(
            id=self.import_excel, children=html.Div("Upload my Excel"), multiple=False,
        )
        excel_input_div = html.Button(excel_input)
        return excel_input_div

    def exportExcelButton(self):
        export_button = html.Div(
            [
                html.Button("Download Excel", id=self.export_excel_button, n_clicks=0),
                dcc.Download(id=self.export_excel),
            ]
        )
        return export_button

    def buttonDiv(self, id: str, children):
        return html.Button(id=id, children=children, n_clicks=0)

    def testDiv(self):
        return html.Div(id=self.test)

    def confirmDialogueDiv(self: str, message: str):
        return dcc.ConfirmDialog(id=self.conf_dial, message=message)
