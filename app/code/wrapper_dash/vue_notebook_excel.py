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

    def getInputDiv(self):
        update_data_div = self.ReusableStandardButtons.getUpdateDataDiv()
        update_msg_box = self.ReusableOutputs.getMessageToUserDiv()
        update_div = html.Div(children=[update_data_div, update_msg_box])

        edit_button = self.ReusableStandardButtons.getEditButtonsAndColumnsDiv()
        upload_excel_div = self.ReusableStandardButtons.getImportExcelDiv()
        upload_msg_box_upload_excel = self.ReusableOutputs.getMessageToUserImportExcelInfoDiv()
        upload_div = html.Div(children=[upload_excel_div, upload_msg_box_upload_excel])

        update_div_formated = html.Div(  
            children=[
                edit_button,
                update_div,
                upload_div
                ],
            style={
                    "display":"flex",
                    "justify-content":"space-between"
                    }
            )


        return update_div_formated
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
        return self.ReusableNotebook.getDashNotebookCallbackAsStateData()
    def getNotebookCallbackAsStateColumn(self):
        return self.ReusableNotebook.getDashNotebookCallbackAsStateColumns()

    def getMessageToUserUpdateCallback(self):
        return self.ReusableOutputs.getMessageToUserCallback()
    def getMessageToUserImportExcelInfoCallback(self):
        return self.ReusableOutputs.getMessageToUserImportExcelInfoCallback()

    
    def getAddRowDiv(self):
        return html.Button('Add Row', id='add-rows-button-notebook', n_clicks=0)
    def getAddRowCallback(self):
        return Input('add-rows-button-notebook', 'n_clicks')




class EmptyVue():
    def __init__(self, ExcelToDataframe, ConfigNotebookExcelSaver, StandardButtonsConfigSaver):
        self.name_vue = "notebook-excel-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableOutputs = reusable_outputs.ReusableOutputs(self.name_vue)
        self.ReusableNotebook = reusable_notebook.ReusableNotebook(self.name_vue, ExcelToDataframe, ConfigNotebookExcelSaver)
        self.ReusableStandardButtons = reusable_standard_buttons.ReusableStandardButtons(self.name_vue, StandardButtonsConfigSaver)

        self.StandardButtonsConfigSaver = StandardButtonsConfigSaver

        self.elementsVue = ElementsVue(ExcelToDataframe, self.ReusableInputs, self.ReusableOutputs, self.ReusableNotebook, self.ReusableStandardButtons)
        
    def getEmptyVue(self):
        input_div = self.elementsVue.getInputDiv()
        # output_div = self.elementsVue.getOutputDiv()
        excel_notebook = self.elementsVue.getNotebookDiv()
        add_row_div = self.elementsVue.getAddRowDiv()

        total_vue = html.Div([input_div, excel_notebook, add_row_div])
        return total_vue


    def getUpdateInputCallbacks(self):
        return self.elementsVue.getInputCallbacks()
    def getNotebookAsInputCallback(self):
        return self.elementsVue.getNotebookCallback()
    def getAddRowCallback(self):
        return self.elementsVue.getAddRowCallback()

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
    def __init__(self, app, ExcelToDataframe, FileSaver, ConfigNotebookExcelSaver, StandardButtonsConfigSaver):
        super().__init__(ExcelToDataframe, ConfigNotebookExcelSaver, StandardButtonsConfigSaver)
        self.app = app
        self.FileSaver = FileSaver
        self.ConfigNotebookExcelSaver = ConfigNotebookExcelSaver

        self._counter_copied_excel = 0
        self._counter_add_row = 0
        self._content_editable = ""

        self.setCallback()

    
    def setCallback(self):
        @self.app.callback(
            self.getMessageToUserUpdateCallback(),
            [self.getNotebookAsInputCallback(), self.getUpdateInputCallbacks()],
            [self.getNotebookCallbackAsStateColumn()]
            )
        # def update_notebook(selected_date_str, selected_periode, imported_excel, data_excel):
        def update_copied_excel(data_notebook, n_clicks_submit, columns_notebook):
            if self._counter_copied_excel != n_clicks_submit:
                self._counter_copied_excel == n_clicks_submit
                # message_to_user = self.FileSaver.saveTemporaryRawExcelFromInputData(data_notebook) # prend de la puissance de calcul parce que sauvegarde a chaque interaction
                
                # print(update_button_state)
                # self.ConfigNotebookExcelSaver.updateColumnsName(columns_notebook)
                message_to_user = "done"
                self.ReusableStandardButtons.saveAllButtons()

                return message_to_user
            return ""


        @self.app.callback(
            [self.getMessageToUserImportExcelInfoCallback(), self.getNotebookAsOutputCallback()],
            [self.ReusableStandardButtons.inputCallback_ImportExcel_contents(), self.getAddRowCallback()],
            self.getNotebookCallbackAsStateData(),
            self.getNotebookCallbackAsStateColumn()
            )
        def import_excel_and_update_notebook(imported_excel, add_row_n_clicks, data_notebook, columns_notebook):   
            message_to_user = ""
            data_for_output = data_notebook

            if imported_excel != None:
                # Save the imported excel, if there is one to save
                message_to_user = self.FileSaver.saveImportedFile(imported_excel)
                # Update the imported excel, if there is an imported excel present

                # dataframme = self.AccessExcel.getDataframeOfRawExcel()
                dataframme = self.ReusableNotebook.getDataframe()
                data_for_output = self.FileSaver.translateDataframeToData(dataframme)
            
            if self._counter_add_row != add_row_n_clicks:
                self._counter_add_row = add_row_n_clicks
                next_id = data_notebook[-1]["ID"]+1
                print(next_id)
                data_notebook.append({
                    c['id']:('' if c['id'] != "ID" else next_id)
                    for c in columns_notebook 
                    })
                message_to_user = "all is ok" 
                data_for_output = data_notebook

            return message_to_user, data_for_output





        @self.app.callback(
            self.ReusableStandardButtons.outputcallbackToMakeAllButtonsEditable(),
            self.ReusableStandardButtons.inputcallbackToMakeAllButtonsEditable(),
            self.ReusableStandardButtons.statecallbackToMakeAllButtonsEditable(),
            )
        def editate_all_buttons(check_value, upd_data_t, ed_col_t, imp_ex_t):  
            if check_value != None:
                if check_value == ["checked"]:
                    return self.ReusableStandardButtons.outputStartEditateButtons()
                # This case means that the checkbox has been unchecked
                elif check_value == []:
                    texts_to_save = [upd_data_t, ed_col_t, imp_ex_t]
                    list_ids = self.ReusableStandardButtons.id_statecallbackToMakeAllButtonsEditable()

                    self.StandardButtonsConfigSaver.saveListIdsListChildren(list_ids, texts_to_save)
                    return self.ReusableStandardButtons.outputEndEditateButtons()

            return self.ReusableStandardButtons.outputEndEditateButtons()
        


    def setThisVue(self):
        return self.getEmptyVue()
