import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_outputs as reusable_outputs
import wrapper_dash.reusable_components.reusable_styles as reusable_styles

import pandas as pd


class UniqueReusableSingleStandardButtons():
    def __init__(self, name_vue, StandardButtonsConfigSaver):
        self.name_vue = name_vue

        self.ReusableSingleInputs = reusable_inputs.ReusableSingleInputs("button-"+self.name_vue)
        self.ReusableSingleOutputs = reusable_outputs.ReusableSingleOutputs("button-"+self.name_vue)

        self.StandardButtonsConfigSaver = StandardButtonsConfigSaver
        self.ReusableStyles = reusable_styles.ReusableStyles()

        self._conf = self.getConfig()
        self.add_div_div = self.name_vue+'add-div'
        self.remove_div_div = self.name_vue+'remove-div'

        # self.UniqueReusableSingleInputs = reusable_inputs.UniqueReusableSingleInputs("-button-"+self.name_vue)
        # self.UniqueReusableSingleOutputs = reusable_outputs.UniqueReusableSingleOutputs("-button-"+self.name_vue)


    def getConfig(self):
        return self.StandardButtonsConfigSaver.getConfig()

    def setConfig(self, data):
        return self.StandardButtonsConfigSaver.setConfig(data)

    # def get


class ReusableSingleStandardButtons(UniqueReusableSingleStandardButtons):
    def __init__(self, name_vue, StandardButtonsConfigSaver):
        super().__init__(name_vue, StandardButtonsConfigSaver)

        self.edit_button = "edit-button"
        self.edit_button_text = self.edit_button+"-text"
        self.update_id = 'update-button'
        self.update_text_id = self.update_id+"-text"
        self.update_msg_div = self.update_id + "-message"

        self.import_excel_id = 'upload-data'
        self.import_excel_text_id = self.import_excel_id+"-text"
        self.import_excel_msg_div = self.import_excel_id + "-message"




    def getEditButtonsAndColumnsChecklist(self):
        edit_button_div = dcc.Checklist(
            id=self.edit_button,
            options=[{"label":"", "value":"checked"}],
            style=  {
                "margin-top": "8px",
                "margin-left": "10px",
            }
        )
        return edit_button_div     
    def inputCallback_EditButtonsAndColumns_value(self):
        callback = Input(self.edit_button, 'value')
        return callback  

    def getEditButtonsAndColumnsTextDiv(self):
        id_text_div = self.edit_button_text
        text_div = dcc.Input(
            id=id_text_div,
            value=self._conf[id_text_div]["value"],
            disabled=True,
            style=self.ReusableStyles.styleStandardPlainText()
        )
        return text_div           
    def outputCallback_EditButtonsAndColumnsText_disabled(self):
        callback = Output(self.edit_button_text, 'disabled')
        return callback
    def stateCallback_EditButtonsAndColumns_text(self):
        callback = State(self.edit_button_text, 'value')
        return callback





    def getMessageToUserUpdateDiv(self):
        output_div = dcc.Input(
            id=self.update_msg_div,
            value='',
            style=self.ReusableStyles.styleStandardPlainText()
            )
        return output_div
    def outputcallback_MessageToUserUpdate_disabled(self):
        return Output(self.update_msg_div, "disabled")
    def outputcallback_MessageToUserUpdate_value(self):
        return Output(self.update_msg_div, "value")
    def statecallback_MessageToUserUpdate_value(self):
        return State(self.update_msg_div, "value")


    def getUpdateDataTextDiv(self):
        update_text_id = self.update_text_id
        update_text_div = dcc.Input(
            id=self.update_text_id,
            value=self._conf[update_text_id]["value"],
            disabled=True,
            style=self.ReusableStyles.styleStandardButtonText()
            )
        return update_text_div
    def outputCallback_UpdateDataText_disabled(self):
        callback = Output(self.update_text_id, 'disabled')
        return callback
    def stateCallback_UpdateDataText_value(self):
        callback = State(self.update_text_id, 'value')
        return callback





    def getMessageToUserImportExcelDiv(self):
        output_div = dcc.Input(
            id=self.import_excel_msg_div,
            value='',
            style=self.ReusableStyles.styleStandardPlainText()
            )
        return output_div
    def outputcallback_MessageToUserImportExcel_disabled(self):
        return Output(self.import_excel_msg_div, "disabled")
    def outputcallback_MessageToUserImportExcel_value(self):
        return Output(self.import_excel_msg_div, "value")
    def statecallback_MessageToUserImportExcel_value(self):
        return State(self.import_excel_msg_div, "value")

    def getImportExcelTextDiv(self):
        excel_text_id = self.import_excel_text_id
        excel_text_div = dcc.Input(
            id=excel_text_id,
            value=self._conf[excel_text_id]["value"],
            disabled=True,
            style=self.ReusableStyles.styleStandardButtonText()
        )
        return excel_text_div
    def outputCallback_ImportExcelText_disabled(self):
        callback = Output(self.import_excel_text_id, 'disabled')
        return callback
    def stateCallback_ImportExcelText_value(self):
        callback = State(self.import_excel_text_id, 'value')
        return callback


    def getImportExcelUpload(self):
        excel_input_id = self.import_excel_id
        excel_input = dcc.Upload(
            id=excel_input_id,
            children=self.getImportExcelTextDiv(),
            multiple=False,
        )
        return excel_input
    def inputCallback_ImportExcel_contents(self):
        callback = Input(self.import_excel_id, 'contents')
        return callback
    def outputCallback_ImportExcel_disabled(self):
        callback = Output(self.import_excel_id, 'disabled')
        return callback



class ReusableStandardButtons(ReusableSingleStandardButtons):
    def __init__(self, name_vue, StandardButtonsConfigSaver, ImportExcelFileSaver=None):
        super().__init__(name_vue, StandardButtonsConfigSaver)
        # self.ReusableInputs = reusable_inputs.ReusableInputs("-button-"+self.name_vue)
        self.ReusableOutputs = reusable_outputs.ReusableOutputs(self.name_vue)

        self.EditButtons = EditButtons(self)
        self.UpdateButton = UpdateButton(self)
        if ImportExcelFileSaver != None:
            self.ImportExcel = ImportExcel(self, ImportExcelFileSaver)




    def getEditButtonsAndColumnsDiv(self):
        edit_button_div = self.getEditButtonsAndColumnsChecklist()
        text_div = self.getEditButtonsAndColumnsTextDiv()
        all_div = html.Div(
            children=[edit_button_div, text_div],
            style={
                    "display":"flex",
                    }
            )   
        return all_div




    def getImportExcelDiv(self):
        excel_input = self.getImportExcelUpload()
        excel_input_div = html.Button(
            children=excel_input,
            style=self.ReusableStyles.syleSimpleFlex()
            )
        excel_msg_div = self.getMessageToUserImportExcelDiv()
        excel_div = html.Div(
            children=[excel_input_div,excel_msg_div],
            style=self.ReusableStyles.syleSimpleFlex()
        )
        return excel_div





    def getUpdateDataDiv(self):
        update_input_id = self.update_id
        update_input = html.Button(
            id=update_input_id,
            children=self.getUpdateDataTextDiv(),
            n_clicks=0,
        )
        message_to_user = self.getMessageToUserUpdateDiv()
        all_div = html.Div(
            children=[update_input, message_to_user],
            style=self.ReusableStyles.syleSimpleFlex()
        )
        return all_div
    def inputCallback_UpdateData_n_clicks(self):
        callback = Input(self.update_id, 'n_clicks')
        return callback
    def outputCallback_UpdateData_disabled(self):
        callback = Output(self.update_id, 'disabled')
        return callback




class EditButtons():
    def __init__(self, ReusableStandardButtons):
        self.ReusableStandardButtons = ReusableStandardButtons

    def outputcallbackToMakeAllButtonsEditable(self):
        outputs = [
            self.ReusableStandardButtons.outputCallback_UpdateDataText_disabled(),
            self.ReusableStandardButtons.outputcallback_MessageToUserUpdate_disabled(),

            self.ReusableStandardButtons.outputCallback_EditButtonsAndColumnsText_disabled(),

            self.ReusableStandardButtons.outputCallback_ImportExcelText_disabled(),
            self.ReusableStandardButtons.outputcallback_MessageToUserImportExcel_disabled(),



            self.ReusableStandardButtons.outputCallback_UpdateData_disabled(),
            self.ReusableStandardButtons.outputCallback_ImportExcel_disabled()
                ]
        return outputs
    def inputcallbackToMakeAllButtonsEditable(self):
        inputs = [
            self.ReusableStandardButtons.inputCallback_EditButtonsAndColumns_value()
        ]
        return inputs
    def statecallbackToMakeAllButtonsEditable(self):
        states = [
                self.ReusableStandardButtons.stateCallback_UpdateDataText_value(),
                self.ReusableStandardButtons.stateCallback_EditButtonsAndColumns_text(),
                self.ReusableStandardButtons.stateCallback_ImportExcelText_value(),

                self.ReusableStandardButtons.statecallback_MessageToUserUpdate_value(),
                self.ReusableStandardButtons.statecallback_MessageToUserImportExcel_value()
                ]
        return states
    def id_statecallbackToMakeAllButtonsEditable(self):
        list_ids = [
            self.ReusableStandardButtons.update_text_id,
            self.ReusableStandardButtons.edit_button_text,
            self.ReusableStandardButtons.import_excel_text_id,

            self.ReusableStandardButtons.update_msg_div,
            self.ReusableStandardButtons.import_excel_msg_div
        ]
        return list_ids

    def outputStartEditButtons(self):
        return False,False,False,False,False, True,True

    def outputEndEditButtons(self):
        return True,True,True,True,True, False,False

    # Main part to do the actions on check/uncheck of the checkbox
    def outputcallbacks(self):
        return self.outputcallbackToMakeAllButtonsEditable()
    def inputcallbacks(self):
        return self.inputcallbackToMakeAllButtonsEditable()
    def statecallbacks(self):
        return self.statecallbackToMakeAllButtonsEditable()

    def edit_buttons(self, check_value, upd_data_t, ed_col_t, imp_ex_t,  msg_user_update, msg_user_import):  
        if check_value != None:
            if check_value == ["checked"]:
                return self.outputStartEditButtons()
            # This case means that the checkbox has been unchecked
            elif check_value == []:
                texts_to_save = [upd_data_t, ed_col_t, imp_ex_t, msg_user_update, msg_user_import]
                list_ids = self.id_statecallbackToMakeAllButtonsEditable()

                self.ReusableStandardButtons.StandardButtonsConfigSaver.saveListIdsListChildren(list_ids, texts_to_save)
                return self.outputEndEditButtons()

        return self.outputEndEditButtons()



class ImportExcel():
    def __init__(self, ReusableStandardButtons, ImportExcelFileSaver):        
        self.ReusableStandardButtons = ReusableStandardButtons
        self.ImportExcelFileSaver = ImportExcelFileSaver


    # Part to do the actions on check/uncheck of the checkbox
    def outputcallbacks(self):
        return self.ReusableStandardButtons.outputcallback_MessageToUserImportExcel_value()
    def inputcallbacks(self):
        return self.ReusableStandardButtons.inputCallback_ImportExcel_contents()
    # def statecallback(self):

    def import_excel(self, imported_excel):   
        message_to_user = ""
        if imported_excel != None:
            # Save the imported excel, if there is one to save
            message_to_user = self.ImportExcelFileSaver.saveImportedFile(imported_excel)
            self.ImportExcelFileSaver.updateDbs()
            # Update the imported excel
        data_for_output = self.getNotebookData()
        return message_to_user, data_for_output


    def changeFormatOfDataframe(self, dataframe):
        try:
            dataframe["Date"] = pd.to_datetime(dataframe["Date"]).dt.strftime('%Y-%m-%d')
            return dataframe
        except Exception as e:
            return dataframe

    def getDataframe(self):
        dataframe =  self.ImportExcelFileSaver.ExcelToDataframe.getDataframeOfRawExcel()
        dataframe = self.changeFormatOfDataframe(dataframe)
        return dataframe

    def translateDataframeToNotebookData(self, dataframe):
        data_for_output = dataframe.to_dict('records')
        return data_for_output

    def getNotebookData(self):
        dataframe = self.getDataframe()
        data_for_output = self.translateDataframeToNotebookData(dataframe)
        return data_for_output



class UpdateButton():
    def __init__(self, ReusableStandardButtons):
        self.ReusableStandardButtons = ReusableStandardButtons

    # 
    def outputcallbacks(self):
        return self.ReusableStandardButtons.outputcallback_MessageToUserUpdate_value()
    def inputcallbacks(self):
        return self.ReusableStandardButtons.inputCallback_UpdateData_n_clicks()


