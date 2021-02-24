import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, State


import datetime
from dateutil.relativedelta import *




class UniqueReusableSingleInputs():
    def __init__(self, name_vue):
        self.name_vue = name_vue

        self.add_div_div = self.name_vue+'add-div'
        self.remove_div_div = self.name_vue+'remove-div'

    def getCallbackClicksOf(self, id_div):
        callback = Input(id_div, 'n_clicks')
        return callback

    def getAddDivDiv(self, name_div, div_children):
        id_div = self.add_div_div+name_div
        add_div = html.Button(
            id=self.add_div_div,
            children=div_children,
            n_clicks=0
        )
        return add_div, id_div

    def getRemoveDivDiv(self, name_div, div_children):
        id_div = self.remove_div_div+name_div
        remove_div = html.Button(
            id=id_div,
            children=div_children,
            n_clicks=0
        )
        return remove_div, id_div



class ReusableSingleInputs(UniqueReusableSingleInputs):
    def __init__(self, name_vue):
        super().__init__(name_vue)

        self.date_div_period_id = self.name_vue+"input-radio"
        self.date_div_date_id = self.name_vue+"input-date"
        self.import_excel_id = self.name_vue+'upload-data'
        self.submit_id = self.name_vue+'submit-button'
        self.location_id = 'default-url'
        self.add_div_div = self.name_vue+'add-div'
        self.remove_div_div = self.name_vue+'remove-div'



    def getDateDiv(self):
        date_input = dcc.DatePickerSingle(
            self.date_div_date_id,
            date = datetime.datetime(year=2019,month=9,day=1),
            # date = datetime.datetime.today()-relativedelta(months=5),
            display_format="D/M/Y"
        )
        return date_input
    def getDateCallback(self):
        return Input(self.date_div_date_id, 'date')


    def getPeriodDiv(self):
        periode_input = dcc.RadioItems(
            self.date_div_period_id,
            options=[
                {"label":"Week", "value":"week"},
                {"label":"Month", "value":"month"},
                {"label":"Quarter", "value":"semestre"}
            ],
            value='month'
        )
        return periode_input
    def getPeriodCallback(self):
        return Input(self.date_div_period_id, 'value')



    def getImportExcelDiv(self):
        excel_input = dcc.Upload(
            id=self.import_excel_id,
            children=html.Div('Import excel File'),
            multiple=False
        )
        excel_input_div = html.Button(excel_input)
        return excel_input_div
    def getImportExcelCallback(self):
        callback = Input(self.import_excel_id, 'contents')
        return callback

    def getUpdateDataDiv(self):
        update_input = html.Button(
            id=self.submit_id,
            children='Update/Submit data',
            n_clicks=0
        )
        return update_input
    def getUpdateDataCallback(self):
        callback = Input(self.submit_id, 'n_clicks')
        return callback


    def getLocationDiv(self):
        location_div = dcc.Location(self.location_id, refresh=False)
        return location_div        
    def getLocationCallback(self):
        callback = Input(self.location_id, 'pathname')
        return callback










class ReusableInputs(ReusableSingleInputs, UniqueReusableSingleInputs):
    def __init__(self, name_vue):
        super().__init__(name_vue)

    def getDatePeriodDiv(self):
        periode_input = self.getPeriodDiv()
        date_input = self.getDateDiv()
        date_input_div = html.Div(  children=[date_input, periode_input],
                                    style={
                                        "display":"flex",
                                        "justify-content":"space-between"})
        return date_input_div
    def getDatePeriodCallbacks(self):
        list_callbacks = [
            self.getDateCallback(),
            self.getPeriodCallback(),
            ]
        return list_callbacks

    def getDatePeriodAndExcelDiv(self):
        date_period_div = self.getDatePeriodDiv()
        import_excel_div = self.getImportExcelDiv()
        all_divs = html.Div(
            children=[date_period_div, import_excel_div],
            style={
                "display":"flex",
                "justify-content":"space-between"}
        )
        return all_divs

    def getDatePeriodAndExcelCallbacks(self):
        date_period_callbacks = self.getDatePeriodCallbacks()
        import_excel_callbacks = self.getImportExcelCallback()

        list_callbacks = [callback for callback in date_period_callbacks]
        list_callbacks.append(import_excel_callbacks)

        return list_callbacks



