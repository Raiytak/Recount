import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import datetime


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_outputs as reusable_outputs
import wrapper_dash.reusable_components.reusable_notebook as reusable_notebook




class ElementsVue():
    def __init__(self, ExcelToDataframe, ReusableInputs, ReusableOutputs, ReusableNotebook):
        self.ReusableInputs = ReusableInputs
        self.ReusableOutputs = ReusableOutputs
        self.ExcelToDataframe = ExcelToDataframe
        self.ReusableNotebook = ReusableNotebook

    def getInputDiv(self):
        update_div = self.ReusableInputs.getUpdateDataDiv()
        update_msg_box = self.ReusableOutputs.getMessageToUserDiv()
        update_div = html.Div(children=[update_div, update_msg_box])

        upload_excel_div = self.ReusableInputs.getImportExcelDiv()
        upload_msg_box_upload_excel = self.ReusableOutputs.getMessageToUserImportExcelInfoDiv()
        upload_div = html.Div(children=[upload_excel_div, upload_msg_box_upload_excel])

        update_div_formated = html.Div(  
            children=[
                update_div,
                upload_div
                ],
            style={
                    "display":"flex",
                    "justify-content":"space-around"})
        return update_div_formated
    def getInputCallbacks(self):
        return self.ReusableInputs.getUpdateDataCallback()

    def getNotebookDiv(self):
        notebook_excel = self.ReusableNotebook.getDashNotebookDiv()
        notebook_excel_div = html.Div(id="notebook-excel", children=notebook_excel)
        return notebook_excel_div
    def getNotebookCallback(self):
        return self.ReusableNotebook.getDashNotebookCallback()
    def getNotebookCallbackAsOutput(self):
        return self.ReusableNotebook.getDashNotebookCallbackAsOutput()

    def getMessageToUserUpdateCallback(self):
        return self.ReusableOutputs.getMessageToUserCallback()
    def getMessageToUserImportExcelInfoCallback(self):
        return self.ReusableOutputs.getMessageToUserImportExcelInfoCallback()

        



class EmptyVue():
    def __init__(self, ExcelToDataframe):
        self.name_vue = "notebook-excel-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableOutputs = reusable_outputs.ReusableOutputs(self.name_vue)
        self.ReusableNotebook = reusable_notebook.ReusableNotebook(self.name_vue, ExcelToDataframe)
        self.elementsVue = ElementsVue(ExcelToDataframe, self.ReusableInputs, self.ReusableOutputs, self.ReusableNotebook)
        
    def getEmptyVue(self):
        input_div = self.elementsVue.getInputDiv()
        # output_div = self.elementsVue.getOutputDiv()
        excel_notebook = self.elementsVue.getNotebookDiv()

        total_vue = html.Div([input_div, excel_notebook])
        return total_vue


    def getUpdateInputCallbacks(self):
        return self.elementsVue.getInputCallbacks()

    def getNotebookAsInputCallback(self):
        return self.elementsVue.getNotebookCallback()

    def getNotebookAsOutputCallback(self):
        return self.elementsVue.getNotebookCallbackAsOutput()

    def getMessageToUserUpdateCallback(self):
        return self.elementsVue.getMessageToUserUpdateCallback()
    def getMessageToUserImportExcelInfoCallback(self):
        return self.elementsVue.getMessageToUserImportExcelInfoCallback()




# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, ExcelToDataframe, FileSaver):
        super().__init__(ExcelToDataframe)
        self.app = app
        self.ExcelToDataframe = ExcelToDataframe
        self.AccessExcel = self.ExcelToDataframe.AccessExcel
        self.FileSaver = FileSaver

        self._counter = 0

        self.setCallback()

    
    def setCallback(self):
        @self.app.callback(
            self.getMessageToUserUpdateCallback(),
            [self.getNotebookAsInputCallback(), self.getUpdateInputCallbacks()]
            )
        # def update_notebook(selected_date_str, selected_periode, imported_excel, data_excel):
        def update_data(data_excel, n_clicks_submit):
            if self._counter != n_clicks_submit:
                print("data submited")
                print(n_clicks_submit)
                self._counter == n_clicks_submit
                message_to_user = self.FileSaver.saveTemporaryRawExcelFromInputData(data_excel) # prend de la puissance de calcul parce que sauvegarde a chaque interaction
                return message_to_user
            return ""


        @self.app.callback(
            [self.getMessageToUserImportExcelInfoCallback(), self.getNotebookAsOutputCallback()],
            self.ReusableInputs.getImportExcelCallback())
        def update_notebook(imported_excel):     
            # Save the imported excel, if there is one to save
            message_to_user = self.FileSaver.saveImportedFile(imported_excel)
            # Update the imported excel, if there is an imported excel present

            # dataframme = self.AccessExcel.getDataframeOfRawExcel()
            dataframme = self.ReusableNotebook.getDataframe()
            data_for_output = self.FileSaver.translateDataframeToData(dataframme)
            
            return message_to_user, data_for_output


    def setThisVue(self):
        return self.getEmptyVue()
