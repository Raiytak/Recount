import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, State


import datetime
from dateutil.relativedelta import *






class ReusableSingleOutputs():
    def __init__(self, name_vue):
        self.name_vue = name_vue

        self.msg_div = self.name_vue+"message-to-user"
        self.msg_import_excel_div = self.name_vue+"message-to-user--import-excel"





    def getMessageToUserDiv(self):
        output_div = html.P(id=self.msg_div, children='')
        return output_div
    def getMessageToUserCallback(self):
        return Output(self.msg_div, "children")

    def getMessageToUserImportExcelInfoDiv(self):
        output_div = html.P(id=self.msg_import_excel_div, children='')
        return output_div
    def getMessageToUserImportExcelInfoCallback(self):
        return Output(self.msg_import_excel_div, "children")




class ReusableOutputs(ReusableSingleOutputs):
    def __init__(self, name_vue):
        super().__init__(name_vue)



