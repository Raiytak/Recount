import logging
from dash import dcc, html, Input, Output


import datetime
from dateutil.relativedelta import *


from .css_style import *


class RecountInputs:
    def __init__(self, name_vue):
        self.date_div_period_id = name_vue + "-input-radio"
        self.date_div_date_id = name_vue + "-input-date"
        self.import_excel_id = name_vue + "-import-excel"
        self.submit_id = name_vue + "-submit-button"

        self.reset_button = name_vue + "-reset-button"
        self.reset_output = name_vue + "-reset-output"
        self.conf_dial = name_vue + "-confirm-dialog"

        self.export_excel = name_vue + "-export-excel"
        self.export_excel_button = name_vue + "-export-excel-button"

        self.location_id = name_vue + "-default-url"

        self.add_div_div = name_vue + "-add-div"
        self.remove_div_div = name_vue + "-remove-div"

        self.edit_buttons_id = name_vue + "-edit-buttons-div"

    def dashboardInputDiv(self):
        date_period_div = self.datePeriodDiv()
        reset_button = self.resetUserData()
        import_excel = self.importExcelButton()
        export_excel = self.exportExcelButton()
        import_export_div = html.Div(
            children=[import_excel, export_excel], style=flexColumn
        )
        buttons_div = html.Div(children=[reset_button, import_export_div], style=flex)
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

    def periodCallback(self):
        return Input(self.date_div_period_id, "value")

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

    def dateCallback(self):
        return Input(self.date_div_date_id, "date")

    def resetUserData(self):
        return html.Div(
            children=[
                html.Button(id=self.reset_button, children="Reset My Data", n_clicks=0),
                html.Div(id=self.reset_output),
            ],
            style=flexColumn,
        )

    def resetUserDataButtonCallback(self):
        return Input(self.reset_button, "n_clicks")

    def importExcelButton(self):
        excel_input = dcc.Upload(
            id=self.import_excel_id,
            children=html.Div("Upload my Excel"),
            multiple=False,
        )
        excel_input_div = html.Button(excel_input)
        return excel_input_div

    def importExcelCallback(self):
        callback = Input(self.import_excel_id, "contents")
        return callback

    def exportExcelButton(self):
        export_button = html.Div(
            [
                html.Button("Download Excel", id=self.export_excel_button, n_clicks=0),
                dcc.Download(id=self.export_excel),
            ]
        )
        return export_button

    def exportExcelButtonCallback(self):
        logging.info(
            "setting exportExcelButtonCallback: {}".format(self.export_excel_button)
        )
        return Input(self.export_excel_button, "n_clicks")

    def confirmDialogueInput(self):
        return Input(self.conf_dial, "n_clicks")


# class UniqueReusableSingleInputs:
#     def __init__(self, name_vue):
#         self.name_vue = name_vue

#         self.add_div_div = self.name_vue + "add-div"
#         self.remove_div_div = self.name_vue + "remove-div"

#     def getCallbackClicksOf(self, id_div):
#         callback = Input(id_div, "n_clicks")
#         return callback

#     def getAddDivDiv(self, name_div, div_children):
#         id_div = self.add_div_div + name_div
#         add_div = html.Button(id=self.add_div_div, children=div_children, n_clicks=0)
#         return add_div, id_div

#     def getRemoveDivDiv(self, name_div, div_children):
#         id_div = self.remove_div_div + name_div
#         remove_div = html.Button(id=id_div, children=div_children, n_clicks=0)
#         return remove_div, id_div


# class ReusableSingleInputs(UniqueReusableSingleInputs):
#     def __init__(self, name_vue):
#         super().__init__(name_vue)

#         self.date_div_period_id = self.name_vue + "input-radio"
#         self.date_div_date_id = self.name_vue + "input-date"
#         self.import_excel_id = self.name_vue + "import-excel"
#         self.submit_id = self.name_vue + "submit-button"
#         self.reset_user = self.name_vue + "reset-user"
#         self.export_excel = self.name_vue + "export-excel"
#         self.export_excel_button = self.name_vue + "export-excel-button"

#         self.location_id = "default-url"

#         self.add_div_div = self.name_vue + "add-div"
#         self.remove_div_div = self.name_vue + "remove-div"

#         self.edit_buttons_id = self.name_vue + "edit-buttons-div"

#     def getDateDiv(self):
#         date_input = dcc.DatePickerSingle(
#             self.date_div_date_id,
#             date=datetime.datetime(year=2019, month=9, day=1),
#             # date = datetime.datetime.today()-relativedelta(months=5),
#             display_format="D/M/Y",
#         )
#         return date_input

#     def getDateCallback(self):
#         return Input(self.date_div_date_id, "date")

#     def getPeriodDiv(self):
#         period_input = dcc.RadioItems(
#             self.date_div_period_id,
#             options=[
#                 {"label": "Week", "value": "week"},
#                 {"label": "Month", "value": "month"},
#                 {"label": "Quarter", "value": "semestre"},
#                 {"label": "Annual", "value": "annual"},
#             ],
#             value="month",
#             style={"fontSize": "medium"},
#         )
#         return period_input

#     def getPeriodCallback(self):
#         return Input(self.date_div_period_id, "value")

#     def getImportExcelButton(self):
#         excel_input = dcc.Upload(
#             id=self.import_excel_id,
#             children=html.Div("Upload my Excel"),
#             multiple=False,
#         )
#         excel_input_div = html.Button(excel_input)
#         return excel_input_div

#     def getImportExcelCallback(self):
#         callback = Input(self.import_excel_id, "contents")
#         return callback

#     def getImportExcelStateCallback(self):
#         callback = State(self.import_excel_id, "children")
#         return callback

#     def getResetUserData(self):
#         reset_button = html.Button(
#             id=self.reset_user, children="Reset My Data", n_clicks=0
#         )
#         return reset_button

#     def getResetUserDataCallback(self):
#         callback = Input(self.reset_user, "n_clicks")
#         return callback

#     def getExportExcelButton(self):
#         reset_button = html.Div(
#             [
#                 html.Button("Download Excel", id=self.export_excel_button),
#                 dcc.Download(id=self.export_excel),
#             ]
#         )
#         return reset_button

#     def getExportExcelInputCallback(self):
#         callback = Input(self.export_excel_button, "n_clicks")
#         return callback

#     def getExportExcelOutputCallback(self):
#         callback = Output(self.export_excel, "data")
#         return callback

#     def getUpdateDataDiv(self):
#         update_input = html.Button(
#             id=self.submit_id,
#             children="Update",
#             n_clicks=0,
#             contentEditable="False",
#             disabled=False,
#         )
#         return update_input

#     def getUpdateDataCallback(self):
#         callback = Input(self.submit_id, "n_clicks")
#         return callback

#     def getUpdateDataStateCallback(self):
#         callback = State(self.submit_id, "children")
#         return callback

#     def getSaveConfigDiv(self):
#         update_input = html.Button(
#             id=self.submit_id, children="Save Shape", n_clicks=0, editable=True
#         )
#         return update_input

#     def getSaveConfigCallback(self):
#         callback = Input(self.submit_id, "n_clicks")
#         return callback

#     def getLocationDiv(self):
#         location_div = dcc.Location(self.location_id, refresh=True)
#         return location_div

#     def getLocationCallback(self):
#         callback = Input(self.location_id, "pathname")
#         return callback

#     def getEditButtonsAndColumnsDiv(self):
#         edit_button_div = dcc.Checklist(
#             id=self.edit_buttons_id, options=[{"label": "Edit", "value": "checked"}]
#         )
#         return edit_button_div

#     def getEditButtonsAndColumnsCallback(self):
#         callback = Input(self.edit_buttons_id, "value")
#         return callback


# class ReusableInputs(ReusableSingleInputs):
#     def __init__(self, name_vue):
#         super().__init__(name_vue)

#     def getDatePeriodDiv(self):
#         period_input = self.getPeriodDiv()
#         date_input = self.getDateDiv()
#         date_input_div = html.Div(
#             children=[date_input, period_input], style=spaceBetween()
#         )
#         return date_input_div

#     def getDatePeriodCallbacks(self):
#         list_callbacks = [self.getDateCallback(), self.getPeriodCallback()]
#         return list_callbacks

#     def getDashboardInputsDiv(self):
#         date_period_div = self.getDatePeriodDiv()
#         reset_button = self.getResetUserData()
#         import_excel = self.getImportExcelButton()
#         export_excel = self.getExportExcelButton()
#         import_export_div = html.Div(
#             children=[import_excel, export_excel], style=syleFlexColumn()
#         )
#         buttons_div = html.Div(
#             children=[reset_button, import_export_div], style=syleFlex()
#         )
#         all_divs = html.Div(
#             children=[date_period_div, buttons_div], style=spaceBetween()
#         )
#         return all_divs

#     def getDatePeriodAndExcelCallbacks(self):
#         date_period_callbacks = self.getDatePeriodCallbacks()
#         import_excel_callbacks = self.getImportExcelCallback()

#         list_callbacks = [callback for callback in date_period_callbacks]
#         list_callbacks.append(import_excel_callbacks)

#         return list_callbacks

#     def getExportResetExcelCallbacks(self):
#         export_callback = self.getExportExcelInputCallback()
#         reset_callback = self.getResetUserDataCallback()

#         return [reset_callback, export_callback]
