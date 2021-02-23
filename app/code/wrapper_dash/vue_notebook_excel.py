import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import datetime


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_notebook as reusable_notebook




class ElementsVue():
    def __init__(self, ExcelToDataframe, ReusableInputs, ReusableNotebook):
        self.ReusableInputs = ReusableInputs
        self.ExcelToDataframe = ExcelToDataframe
        self.ReusableNotebook = ReusableNotebook

    def getInputDiv(self):
        return self.ReusableInputs.getDatePeriodAndExcelDiv()
    def getInputCallbacks(self):
        return self.ReusableInputs.getDatePeriodAndExcelCallbacks()

    def getNotebookDiv(self):
        notebook_excel = self.ReusableNotebook.getDashNotebookDiv()
        notebook_excel_div = html.Div(id="notebook-excel", children=notebook_excel)
        return notebook_excel_div
    def getNotebookCallback(self):
        return self.ReusableNotebook.getDashNotebookCallback()
    def getNotebookCallbackAsOutput(self):
        return self.ReusableNotebook.getDashNotebookCallbackAsOutput()


    def getOutputDiv(self):
        output_div = html.Div(id="output-div")
        return output_div

        



class EmptyVue():
    def __init__(self, ExcelToDataframe):
        self.name_vue = "notebook-excel-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableNotebook = reusable_notebook.ReusableNotebook(self.name_vue, ExcelToDataframe)
        self.elementsVue = ElementsVue(ExcelToDataframe, self.ReusableInputs, self.ReusableNotebook)
        
    def getEmptyVue(self):
        input_div = self.elementsVue.getInputDiv()
        output_div = self.elementsVue.getOutputDiv()
        excel_notebook = self.elementsVue.getNotebookDiv()

        total_vue = html.Div([input_div, output_div, excel_notebook])
        return total_vue


    def getInputCallbacks(self):
        list_callbacks = []
        list_callbacks += self.elementsVue.getInputCallbacks()
        list_callbacks.append(self.elementsVue.getNotebookCallback())
        return list_callbacks

    def getNotebookInputCallback(self):
        return self.elementsVue.getNotebookCallback()

    def getNotebookOutputCallback(self):
        return self.elementsVue.getNotebookCallbackAsOutput()




# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, ExcelToDataframe, FileSaver):
        super().__init__(ExcelToDataframe)
        self.app = app
        self.ExcelToDataframe = ExcelToDataframe
        self.AccessExcel = self.ExcelToDataframe.AccessExcel
        self.FileSaver = FileSaver

        self.setCallback()

    
    def setCallback(self):
        @self.app.callback(
            Output("output-div", "content"),
            self.getNotebookInputCallback())
        # def update_notebook(selected_date_str, selected_periode, imported_excel, data_excel):
        def update_notebook(data_excel):
            # print(type(data_excel))
            # print(data_excel)
            # self.updateCurrentNotebookData(data_excel)
            # self.FileSaver.saveFileTemporary(data_excel) # prend de la puissance de calcul parce que sauvegarde a chaque interaction
            # self.FileSaver.saveImportedFile(imported_excel)

            return ""


        @self.app.callback(
            self.getNotebookOutputCallback(),
            self.ReusableInputs.getImportExcelCallback())
        def update_notebook(imported_excel):     
            # Save the imported excel, if there is one to save
            self.FileSaver.saveImportedFile(imported_excel)
            # Update the imported excel, if there is an imported excel present

            # dataframme = self.AccessExcel.getDataframeOfRawExcel()
            dataframme = self.ReusableNotebook.getDataframe()
            data_for_output = self.FileSaver.translateDataframeToData(dataframme)
            
            return data_for_output


    def setThisVue(self):
        return self.getEmptyVue()
