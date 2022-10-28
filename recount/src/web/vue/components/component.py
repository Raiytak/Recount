import datetime
from dash import html, dcc

from .css_style import *

__all__ = ["RecountComponents", "DefaultButtons", "RecountDefaultDivs"]


class DefaultButtons:
    reset_button = "reset-button"
    confirm_reset_dialogue = "confirm-reset-dialog"
    upload_excel = "upload-excel"
    download_excel = "export-excel"
    download_excel_button = "export-excel-button"
    edit_buttons_id = "edit-buttons-div"

    @classmethod
    def uploadDownloadResetDiv(cls):
        reset_button = html.Button(
            id=cls.reset_button, children="Reset My Data", n_clicks=0
        )
        confirm_reset = cls.confirmResetDialogueDiv(
            message="Are you sure you want to reset your data?"
        )
        upload_excel = cls.uploadButton()
        export_button = cls.downloadButton()
        return html.Div(
            children=[confirm_reset, upload_excel, export_button, reset_button],
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
    def downloadButton(cls):
        download_div = html.Div(
            [
                html.Button("Download Excel", id=cls.download_excel_button, n_clicks=0),
                dcc.Download(id=cls.download_excel),
            ]
        )
        return download_div

    @classmethod
    def confirmResetDialogueDiv(cls: str, message: str):
        return dcc.ConfirmDialog(id=cls.confirm_reset_dialogue, message=message)


class RecountComponents:
    def __init__(self, name_vue, *args, **kwargs):
        self.name_vue = name_vue

        self.loading_div = name_vue + "-loading-page"
        self.test = "test"

        # INPUT
        self.date_div_period_id = name_vue + "-input-radio"
        self.date_div_date_id = name_vue + "-input-date"

        self.add_div_div = name_vue + "-add-div"
        self.remove_div_div = name_vue + "-remove-div"

        # OUTPUT
        self.conf_dial = name_vue + "-confirm-dialog"

        # BUTTON
        self.submit_id = name_vue + "-submit-button"

        # self.hidden_div = name_vue + "-hidden-div"

    def loadingDiv(self):
        loading_page = dcc.Loading(
            type="default", children=[html.Div(id=self.loading_div)],
        )
        return loading_page

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

    def datePeriodDiv(self):
        period_input = self.periodDiv()
        date_input = self.dateDiv()
        date_input_div = html.Div(
            children=[date_input, period_input], style=spaceBetween
        )
        return date_input_div
