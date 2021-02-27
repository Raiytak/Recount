import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import datetime


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_outputs as reusable_outputs
import wrapper_dash.reusable_components.reusable_notebook as reusable_notebook
import wrapper_dash.reusable_components.reusable_standard_buttons as reusable_standard_buttons




class ElementsVue():
    def __init__(self, ExcelToDataframe, ReusableInputs, ReusableOutputs, ReusableNotebook, ReusableStandardButtons):
        self.ReusableInputs = ReusableInputs
        self.ReusableOutputs = ReusableOutputs
        self.ExcelToDataframe = ExcelToDataframe
        self.ReusableNotebook = ReusableNotebook
        self.ReusableStandardButtons = ReusableStandardButtons
        
    def getInputCallbacks(self):
        return self.ReusableStandardButtons.inputCallback_UpdateData_n_clicks()

    def getNotebookDiv(self):
        notebook_excel = self.ReusableNotebook.getDashNotebookDiv()
        notebook_excel_div = html.Div(id="notebook-excel", children=notebook_excel)
        return notebook_excel_div
    def getNotebookCallback(self):
        return self.ReusableNotebook.getDashNotebookCallback()
    def getNotebookCallbackAsOutput(self):
        return self.ReusableNotebook.getDashNotebookCallbackAsOutput()
    def getNotebookCallbackAsStateData(self):
        return self.ReusableNotebook.statecallback_Notebook_data()
    def getNotebookCallbackAsStateColumn(self):
        return self.ReusableNotebook.statecallback_Notebook_columns()

    def getMessageToUserUpdateCallback(self):
        return self.ReusableOutputs.getMessageToUserCallback()
    def getMessageToUserImportExcelInfoCallback(self):
        return self.ReusableOutputs.getMessageToUserImportExcelInfoCallback()





class EmptyVue():
    def __init__(self, ExcelToDataframe, ImportExcelFileSaver, ConfigNotebookExcelSaver, StandardButtonsConfigSaver):
        self.name_vue = "notebook-excel-"
        self.ImportExcelFileSaver = ImportExcelFileSaver
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableOutputs = reusable_outputs.ReusableOutputs(self.name_vue)
        self.ReusableStandardButtons = reusable_standard_buttons.ReusableStandardButtons(self.name_vue, StandardButtonsConfigSaver, self.ImportExcelFileSaver)
        self.ReusableNotebook = reusable_notebook.ReusableNotebook(self.name_vue, ExcelToDataframe, ConfigNotebookExcelSaver, self.ReusableStandardButtons)

        self.StandardButtonsConfigSaver = StandardButtonsConfigSaver

        self.elementsVue = ElementsVue(ExcelToDataframe, self.ReusableInputs, self.ReusableOutputs, self.ReusableNotebook, self.ReusableStandardButtons)
        
    def getEmptyVue(self):
        return self.ReusableNotebook.getEmptyVue()


    def getUpdateInputCallbacks(self):
        return self.ReusableNotebook.getInputCallbacks()
    def getNotebookAsInputCallback(self):
        return self.ReusableNotebook.getNotebookCallback()
    def getAddRowCallback(self):
        return self.ReusableNotebook.getAddRowCallback()

    def getNotebookAsOutputCallback(self):
        return self.elementsVue.getNotebookCallbackAsOutput()
    def getNotebookCallbackAsStateColumn(self):
        return self.elementsVue.getNotebookCallbackAsStateColumn()
    def getNotebookCallbackAsStateData(self):
        return self.elementsVue.getNotebookCallbackAsStateData()

    def getMessageToUserUpdateCallback(self):
        return self.elementsVue.getMessageToUserUpdateCallback()
    def getMessageToUserImportExcelInfoCallback(self):
        return self.elementsVue.getMessageToUserImportExcelInfoCallback()






# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, ExcelToDataframe, ImportExcelFileSaver, ConfigNotebookExcelSaver, StandardButtonsConfigSaver):
        super().__init__(ExcelToDataframe, ImportExcelFileSaver, ConfigNotebookExcelSaver, StandardButtonsConfigSaver)
        self.app = app
        self.ConfigNotebookExcelSaver = ConfigNotebookExcelSaver

        self._counter_copied_excel = 0
        self._counter_add_row = 0

        self.setCallback()

    
    def setCallback(self):
        
        @self.app.callback(
            self.ReusableStandardButtons.UpdateButton.outputcallbacks(),
            self.ReusableStandardButtons.UpdateButton.inputcallbacks(),
            [self.ReusableNotebook.statecallback_Notebook_data(), self.ReusableNotebook.statecallback_Notebook_columns()]
            )
        def do_update(n_clicks_submit, data_notebook, columns_notebook):
            message_to_user = ""
            if self._counter_copied_excel != n_clicks_submit:
                message_to_user = self.ImportExcelFileSaver.saveNotebookDataTorawExcel(data_notebook) 
                self.ConfigNotebookExcelSaver.updateColumnsName(columns_notebook)
            #     self.ImportExcelFileSaver.updateDbs() # prend de la puissance de calcul parce que sauvegarde a chaque interaction
            return message_to_user



        @self.app.callback(
            self.ReusableNotebook.AddRow.outputcallbacks(),
            self.ReusableNotebook.AddRow.inputcallbacks(),
            self.ReusableNotebook.AddRow.statecallbacks()
            )
        def add_row_notebook(add_row_n_clicks, data_notebook, columns_notebook):  
            message_to_user = ""
            data_for_output = data_notebook
            if add_row_n_clicks != self._counter_add_row:
                print("ici")
                self._counter_add_row = add_row_n_clicks
                message_to_user, data_for_output = self.ReusableNotebook.AddRow.add_row_notebook(data_notebook, columns_notebook)
            return message_to_user, data_for_output


        @self.app.callback(
            self.ReusableStandardButtons.ImportExcel.outputcallbacks(),
            self.ReusableStandardButtons.ImportExcel.inputcallbacks()
            )
        def import_excel(imported_excel):  
            message_to_user = ""
            if imported_excel != None:
                message_to_user, data_for_output = self.ReusableStandardButtons.ImportExcel.import_excel(imported_excel)
            return message_to_user


        @self.app.callback(
            self.ReusableStandardButtons.EditButtons.outputcallbacks(),
            self.ReusableStandardButtons.EditButtons.inputcallbacks(),
            self.ReusableStandardButtons.EditButtons.statecallbacks()
            )
        def edit_buttons(check_value, upd_data_t, ed_col_t, imp_ex_t,  msg_user_update, msg_user_import):  
            return self.ReusableStandardButtons.EditButtons.edit_buttons(check_value, upd_data_t, ed_col_t, imp_ex_t,  msg_user_update, msg_user_import)
        


    def setThisVue(self):
        return self.getEmptyVue()
