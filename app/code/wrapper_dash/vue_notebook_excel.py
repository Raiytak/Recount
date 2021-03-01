import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import datetime
import time


import wrapper_dash.reusable_components.reusable_notebook as reusable_notebook
import wrapper_dash.reusable_components.reusable_standard_buttons as reusable_standard_buttons




class ElementsVue():
    def __init__(self):  
        pass



class EmptyVue():
    def __init__(self, ExcelToDataframe, ImportExcelFileSaver, ConfigNotebookExcelSaver, StandardButtonsConfigSaver):
        self.name_vue = "notebook-excel"

        self.ReusableStandardButtons = reusable_standard_buttons.ReusableStandardButtons(self.name_vue, StandardButtonsConfigSaver, ImportExcelFileSaver)
        self.ReusableNotebook = reusable_notebook.ReusableNotebook(self.name_vue, ExcelToDataframe, ConfigNotebookExcelSaver, self.ReusableStandardButtons)

        self.elementsVue = ElementsVue()
        
    def getEmptyVue(self):
        return self.ReusableNotebook.getEmptyVue()





# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, ExcelToDataframe, ImportExcelFileSaver, ConfigNotebookExcelSaver, StandardButtonsConfigSaver):
        super().__init__(ExcelToDataframe, ImportExcelFileSaver, ConfigNotebookExcelSaver, StandardButtonsConfigSaver)
        self.app = app
        self.ConfigNotebookExcelSaver = ConfigNotebookExcelSaver
        self.ImportExcelFileSaver = ImportExcelFileSaver

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
            style_message_to_user = self.ReusableStandardButtons.ReusableStyles.styleStandardPlainTextHidden()
            if self._counter_copied_excel != n_clicks_submit:
                message_import = self.ImportExcelFileSaver.saveNotebookDataTorawExcel(data_notebook) 
                style_message_to_user = self.ReusableStandardButtons.ReusableStyles.styleStandardPlainText()
                self.ConfigNotebookExcelSaver.updateColumnsName(columns_notebook)
            #     self.ImportExcelFileSaver.updateDbs() # prend de la puissance de calcul parce que sauvegarde a chaque interaction
            return style_message_to_user



        @self.app.callback(
            self.ReusableNotebook.AddRow.outputcallbacks(),

            self.ReusableNotebook.AddRow.inputcallbacks(),
            self.ReusableStandardButtons.ImportExcel.inputcallbacks(),

            self.ReusableNotebook.AddRow.statecallbacks()
            )
        def add_row_notebook(add_row_n_clicks, imported_excel, data_notebook, columns_notebook): 
            style_message_to_user = self.ReusableStandardButtons.ReusableStyles.styleStandardPlainTextHidden()
            data_for_output = data_notebook
            if add_row_n_clicks != self._counter_add_row:
                self._counter_add_row = add_row_n_clicks
                message_to_user, data_for_output = self.ReusableNotebook.AddRow.add_row_notebook(data_notebook, columns_notebook)
                style_message_to_user = self.ReusableStandardButtons.ReusableStyles.styleStandardPlainText()
                
            elif imported_excel != None:
                # Update the notebook using imported excel
                time.sleep(2)
                data_for_output = self.ReusableNotebook.getNotebookData()
            return style_message_to_user, data_for_output


        @self.app.callback(
            self.ReusableStandardButtons.ImportExcel.outputcallbacks(),
            self.ReusableStandardButtons.ImportExcel.inputcallbacks()
            )
        def import_excel(imported_excel):  
            message_to_user = ""
            if imported_excel != None:
                message_to_user = self.ReusableStandardButtons.ImportExcel.import_excel(imported_excel)

            return message_to_user


        @self.app.callback(
            self.ReusableStandardButtons.EditButtons.outputcallbacks(),
            self.ReusableStandardButtons.EditButtons.inputcallbacks(),
            self.ReusableStandardButtons.EditButtons.statecallbacks()
            )
        def edit_buttons(check_value):  
            texts_to_save = []
            list_ids = self.ReusableStandardButtons.EditButtons.id_statecallbackToMakeAllButtonsEditable()

            return self.ReusableStandardButtons.EditButtons.edit_buttons(check_value, list_ids, texts_to_save)
        


    def setThisVue(self):
        return self.getEmptyVue()
