import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, State


import datetime
from dateutil.relativedelta import *







class UniqueReusableSingleOutputs():
    def __init__(self, name_vue):
        self.name_vue = name_vue

        self.h1_div_div = self.name_vue+'h1-div'
        self.h2_div_div = self.name_vue+'h2-div'
        self.h3_div_div = self.name_vue+'h3-div'
        self.h4_div_div = self.name_vue+'h4-div'



    def getCallbackChildrenOf(self, id_div):
        callback = Output(id_div, 'children')
        return callback

    def getHDivOfDepth(self, name_div, div_text, depth):
        if depth == 1:
            h_div, h_div_id = self.getH1Div(name_div, div_text)
            return h_div
        if depth == 2:
            h_div, h_div_id = self.getH2Div(name_div, div_text)
            return h_div
        if depth == 3:
            h_div, h_div_id = self.getH3Div(name_div, div_text)
            return h_div
        if depth == 4:
            h_div, h_div_id = self.getH4Div(name_div, div_text)
            return h_div


    def getH1Div(self, name_div, div_text='h1'):
        id_div = self.h1_div_div+name_div
        remove_div = html.Div(
            id=id_div,
            children=div_text,
            contentEditable='True'
        )
        return remove_div, id_div

    def getH2Div(self, name_div, div_text='h2'):
        id_div = self.h2_div_div+name_div+div_text
        remove_div = html.Div(
            id=id_div,
            children=div_text,
            contentEditable='True'
        )
        return remove_div, id_div

    def getH3Div(self, name_div, div_text='h3'):
        id_div = self.h3_div_div+name_div+div_text
        remove_div = html.Div(
            id=id_div,
            children=div_text,
            contentEditable='True'
        )
        return remove_div, id_div

    def getH4Div(self, name_div, div_text='h4'):
        id_div = self.h4_div_div+name_div+div_text
        remove_div = html.Div(
            id=id_div,
            children=div_text,
            contentEditable='True'
        )
        return remove_div, id_div




class ReusableSingleOutputs(UniqueReusableSingleOutputs):
    def __init__(self, name_vue):
        super().__init__(name_vue)

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



