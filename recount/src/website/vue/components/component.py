import datetime
from dash import html, dcc

from .css_style import *

__all__ = ["RecountComponents", "DefaultButtons", "RecountDefaultDivs"]


class DefaultButtons:
    reset_button = "reset-button"
    upload_excel = "upload-excel"
    download_excel = "export-excel"
    download_excel_button = "export-excel-button"
    edit_buttons_id = "edit-buttons-div"

    @classmethod
    def uploadDownloadResetDiv(cls):
        reset_button = html.Button(
            id=cls.reset_button, children="Reset My Data", n_clicks=0
        )
        upload_excel = cls.uploadButton()
        export_button = cls.downloadButton()
        return html.Div(
            children=[upload_excel, export_button, reset_button],
            className="upload-download-reset",
        )

    @classmethod
    def uploadButton(cls):
        upload_component = dcc.Upload(
            id=cls.upload_excel, children=html.Div("Upload my Excel"), multiple=False,
        )
        upload_div = html.Button(upload_component, n_clicks=0)
        return upload_div

    @classmethod
    def downloadButton(self):
        download_div = html.Div(
            [
                html.Button(
                    "Download Excel", id=self.download_excel_button, n_clicks=0
                ),
                dcc.Download(id=self.download_excel),
            ]
        )
        return download_div


class RecountComponents:
    def __init__(self, name_vue, *args, **kwargs):
        self.name_vue = name_vue

        self.location_id = name_vue + "-default-url"
        self.test = "test"

        # INPUT
        self.date_div_period_id = name_vue + "-input-radio"
        self.date_div_date_id = name_vue + "-input-date"

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
        self.submit_id = name_vue + "-submit-button"
        self.update_data_button = name_vue + "-update-data-button"
        self.update_graph_button = name_vue + "-update-graph-button"

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

    def testDiv(self):
        return html.Div(id=self.test)

    def confirmDialogueDiv(self: str, message: str):
        return dcc.ConfirmDialog(id=self.conf_dial, message=message)


class RecountDefaultDivs(RecountComponents, DefaultButtons):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location_id = self.name_vue + "-default-url"
        self.test = "test"

    def datePeriodDiv(self):
        period_input = self.periodDiv()
        date_input = self.dateDiv()
        date_input_div = html.Div(
            children=[date_input, period_input], style=spaceBetween
        )
        return date_input_div

    def dashboardInputDiv(self):
        date_period_div = self.datePeriodDiv()
        refresh_graph_button = html.Button(
            id=self.update_graph_button, children="Refresh Graph", n_clicks=0
        )
        refresh_data_button = html.Button(
            id=self.update_data_button, children="Refresh Data", n_clicks=0
        )

        import_export_reset_div = DefaultButtons.uploadDownloadResetDiv()
        refresh_div = html.Div(
            children=[refresh_graph_button, refresh_data_button], style=flexColumn
        )
        buttons_div = html.Div(
            children=[refresh_div, import_export_reset_div], style=flex
        )
        all_divs = html.Div(children=[date_period_div, buttons_div], style=spaceBetween)
        return all_divs
