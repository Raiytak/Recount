import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import datetime
from dateutil.relativedelta import *


        

class ReusableOutputs(): #TODO
    def __init__(self, name_vue):
        self.name_vue = name_vue

        self.date_div_period_id = self.name_vue+"input-radio"
        self.date_div_date_id = self.name_vue+"input-date"
        self.import_excel_id = self.name_vue+'upload-data'



    def getDatePeriodDiv(self):
        periode_input = dcc.RadioItems(
            id=self.date_div_period_id,
            options=[
                {"label":"Week", "value":"week"},
                {"label":"Month", "value":"month"},
                {"label":"Quarter", "value":"semestre"}
            ],
            value='month'
        )
        date_input = dcc.DatePickerSingle(
            id=self.date_div_date_id,
            # date = datetime.datetime(year=2019,month=9,day=1),
            date = datetime.datetime.today()-relativedelta(months=5),
            display_format="D/M/Y"
        )
        date_input_div = html.Div(  children=[date_input, periode_input],
                                    style={
                                        "display":"flex",
                                        "justify-content":"space-between"})
        return date_input_div
    
    def getDatePeriodCallbacks(self):
        list_callbacks = [
            Input(self.date_div_date_id, 'date'),
            Input(self.date_div_period_id, 'value'),
            ]
        return list_callbacks




    def getImportExcelDiv(self):
        excel_input = dcc.Upload(
            id=self.import_excel_id,
            children=html.Div('Import csv File'),
            multiple=False
        )
        excel_input_div = html.Button(excel_input)
        return excel_input_div
    
    def getImportExcelCallback(self):
        callback = Input(self.import_excel_id, 'contents')
        return callback
        


