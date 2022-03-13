from dash import dcc, html


# from dash.dependencies import Input, Output, State
from .css_style import hidden

from dateutil.relativedelta import *


class RecountOutputs:
    def __init__(self, name_vue):
        self.name_vue = name_vue
        self.h1_div_div = name_vue + "-h1-div"
        self.h2_div_div = name_vue + "-h2-div"
        self.h3_div_div = name_vue + "-h3-div"
        self.h4_div_div = name_vue + "-h4-div"
        self.hidden_div = name_vue + "-hidden-div"
        self.conf_dial = name_vue + "-confirm-dialog"

    def confirmDialogue(self):
        return dcc.ConfirmDialog(
            id=self.conf_dial, message="Are you sure you want to reset your data?"
        )

    def hiddenDiv(self):
        id_div = self.hidden_div
        hidden_div = html.Div(id=id_div, style=hidden)
        return hidden_div


# class UniqueReusableSingleOutputs:
#     def __init__(self, name_vue):
#         self.name_vue = name_vue

#         self.h1_div_div = self.name_vue + "h1-div"
#         self.h2_div_div = self.name_vue + "h2-div"
#         self.h3_div_div = self.name_vue + "h3-div"
#         self.h4_div_div = self.name_vue + "h4-div"
#         self.hidden_div = self.name_vue + "hidden-div"

#     def getCallbackChildrenOf(self, id_div):
#         callback = Output(id_div, "children")
#         return callback

#     def getHDivOfDepth(self, name_div, div_text, depth):
#         if depth == 1:
#             h_div, h_div_id = self.getH1Div(name_div, div_text)
#             return h_div
#         if depth == 2:
#             h_div, h_div_id = self.getH2Div(name_div, div_text)
#             return h_div
#         if depth == 3:
#             h_div, h_div_id = self.getH3Div(name_div, div_text)
#             return h_div
#         if depth == 4:
#             h_div, h_div_id = self.getH4Div(name_div, div_text)
#             return h_div

#     def getH1Div(self, name_div, div_text="h1"):
#         id_div = self.h1_div_div + name_div
#         remove_div = html.Div(id=id_div, children=div_text, contentEditable="True")
#         return remove_div, id_div

#     def getH2Div(self, name_div, div_text="h2"):
#         id_div = self.h2_div_div + name_div + div_text
#         remove_div = html.Div(id=id_div, children=div_text, contentEditable="True")
#         return remove_div, id_div

#     def getH3Div(self, name_div, div_text="h3"):
#         id_div = self.h3_div_div + name_div + div_text
#         remove_div = html.Div(id=id_div, children=div_text, contentEditable="True")
#         return remove_div, id_div

#     def getH4Div(self, name_div, div_text="h4"):
#         id_div = self.h4_div_div + name_div + div_text
#         remove_div = html.Div(id=id_div, children=div_text, contentEditable="True")
#         return remove_div, id_div

#     def getHiddenDiv(self, name_div):
#         id_div = self.hidden_div + name_div
#         hidden_div = html.Div(id=id_div, style={"display": "none"})
#         return hidden_div

#     def getHiddenDivCallback(self, name_div):
#         id_div = self.hidden_div + name_div
#         return Output(id_div, "children")


# class ReusableSingleOutputs(UniqueReusableSingleOutputs):
#     def __init__(self, name_vue):
#         super().__init__(name_vue)
#         self.conf_dial = self.name_vue + "confirm-dialog"
#         self.export_excel = self.name_vue + "export-excel"

#     def getConfirmDialogue(self):
#         return dcc.ConfirmDialog(
#             id=self.conf_dial, message="Are you sure you want to reset your data?"
#         )

#     def getConfirmDialogueCallbacks(self):
#         return (
#             Output(self.conf_dial, "displayed"),
#             Input(self.conf_dial, "submit_n_clicks"),
#         )

#     def getExportExcelButton(self):
#         html.Div(
#             [
#                 html.Button("Download CSV", id="btn_csv"),
#                 dcc.Download(id="download-dataframe-csv"),
#             ]
#         )

#     def getExportExcelCallback(self):
#         callback = Input(self.export_excel, "n_clicks")
#         return callback


# class ReusableOutputs(ReusableSingleOutputs):
#     def __init__(self, name_vue):
#         super().__init__(name_vue)
