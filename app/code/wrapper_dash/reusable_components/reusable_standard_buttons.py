import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_outputs as reusable_outputs




class UniqueReusableSingleStandardButtons():
    def __init__(self, name_vue, StandardButtonsConfigSaver):
        self.name_vue = name_vue

        self.ConfSaver = StandardButtonsConfigSaver
        self._conf = self.getConfig()

        self.add_div_div = self.name_vue+'add-div'
        self.remove_div_div = self.name_vue+'remove-div'

        # self.UniqueReusableSingleInputs = reusable_inputs.UniqueReusableSingleInputs("-button-"+self.name_vue)
        # self.UniqueReusableSingleOutputs = reusable_outputs.UniqueReusableSingleOutputs("-button-"+self.name_vue)


    def getConfig(self):
        return self.ConfSaver.getConfig()

    def setConfig(self, data):
        return self.ConfSaver.setConfig(data)

    # def get


class ReusableSingleStandardButtons(UniqueReusableSingleStandardButtons):
    def __init__(self, name_vue, StandardButtonsConfigSaver):
        super().__init__(name_vue, StandardButtonsConfigSaver)

        self.edit_button = "edit-button"
        self.edit_button_text = self.edit_button+"-text"

        self.submit_id = 'submit-button'
        self.submit_text_id = self.submit_id+"-text"

        self.import_excel_id = 'upload-data'
        self.import_excel_text_id = self.import_excel_id+"-text"

        self.ReusableSingleInputs = reusable_inputs.ReusableSingleInputs("button-"+self.name_vue)
        self.ReusableSingleOutputs = reusable_outputs.ReusableSingleOutputs("button-"+self.name_vue)


    def styleStandardButtonText(self):
        style_standard_button = {
            "display": "inline-block",
            "height": "38px",
            'color': '#555',
            'text-align': 'center',
            'font-size': '11px',
            'font-weight': '600',
            'line-height': '38px',
            'letter-spacing': '.1rem',
            # 'text-transform': 'uppercase',
            'text-decoration': 'none',
            'white-space': 'nowrap',
            'background-color': 'transparent',
            # 'border-radius': '4px',
            'border': '0px',
            'cursor': 'pointer',
            'box-sizing': 'border-box',
            }
        return style_standard_button

    def styleStandardPlainText(self):
        style_standard_button = {
            "display": "inline-block",
            "height": "38px",
            "width": "250px",
            'color': '#555',
            'text-align': 'center',
            'font-size': '11px',
            'font-weight': '600',
            'line-height': '38px',
            'letter-spacing': '.1rem',
            'text-decoration': 'none',
            'white-space': 'nowrap',
            'background-color': 'transparent',
            'box-sizing': 'border-box',
            }
        return style_standard_button

    def getEditButtonsAndColumnsChecklist(self):
        edit_button_div = dcc.Checklist(
            id=self.edit_button,
            options=[{"label":"", "value":"checked"}]
        )
        return edit_button_div     
    def getEditButtonsAndColumnsTextDiv(self):
        id_text_div = self.edit_button_text
        text_div = dcc.Input(
            id=id_text_div,
            value=self._conf[id_text_div]["value"],
            disabled=True,
            style=self.styleStandardPlainText()
        )
        return text_div           
    def inputCallback_EditButtonsAndColumns_value(self):
        callback = Input(self.edit_button, 'value')
        return callback  
    def outputCallback_EditButtonsAndColumns_editable(self):
        callback = Output(self.edit_button_text, 'disabled')
        return callback
    def stateCallback_EditButtonsAndColumns_text(self):
        callback = State(self.edit_button_text, 'value')
        return callback


    def getUpdateDataTextDiv(self):
        submit_text_id = self.submit_text_id
        update_text_div = dcc.Input(
            id=self.submit_text_id,
            value=self._conf[submit_text_id]["value"],
            disabled=True,
            style=self.styleStandardButtonText()
            )
        return update_text_div
    def getUpdateDataDiv(self):
        update_input_id = self.submit_id
        update_input = html.Button(
            id=update_input_id,
            children=self.getUpdateDataTextDiv(),
            n_clicks=0,
        )
        return update_input
    def inputCallback_UpdateData_n_clicks(self):
        callback = Input(self.submit_id, 'n_clicks')
        return callback
    def outputCallback_UpdateData_disabled(self):
        callback = Output(self.submit_id, 'disabled')
        return callback
    def outputCallback_UpdateData_editable(self):
        callback = Output(self.submit_text_id, 'disabled')
        return callback
    def stateCallback_UpdateData_text(self):
        callback = State(self.submit_text_id, 'value')
        return callback



    def getImportExcelTextDiv(self):
        excel_text_id = self.import_excel_text_id
        excel_text_div = dcc.Input(
            id=excel_text_id,
            value=self._conf[excel_text_id]["value"],
            disabled=True,
            style=self.styleStandardButtonText()
        )
        return excel_text_div
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
    def outputCallback_ImportExcel_editable(self):
        callback = Output(self.import_excel_text_id, 'disabled')
        return callback
    def stateCallback_ImportExcel_text(self):
        callback = State(self.import_excel_text_id, 'value')
        return callback





    def getListOfAllButtons(self):
        list_buttons = [
            self.getEditButtonsAndColumnsTextDiv(),
            self.getUpdateDataTextDiv(),
            self.getEditButtonsAndColumnsTextDiv()
        ]
        return list_buttons

    def saveAllButtons(self):
        list_buttons = self.getListOfAllButtons()
        self.ConfSaver.saveListOfDiv(list_buttons)


    def outputcallbackToMakeAllButtonsEditable(self):
        outputs = [
            self.outputCallback_UpdateData_editable(),
            self.outputCallback_EditButtonsAndColumns_editable(),
            self.outputCallback_ImportExcel_editable(),

            self.outputCallback_UpdateData_disabled(),
            self.outputCallback_ImportExcel_disabled()
                ]
        return outputs
    def inputcallbackToMakeAllButtonsEditable(self):
        inputs = [
            self.inputCallback_EditButtonsAndColumns_value()
            # self.inputCallback_UpdateData_text(),
            # self.inputCallback_EditButtonsAndColumns_text(),
            # self.inputCallback_ImportExcel_text(),
        ]
        return inputs
    def statecallbackToMakeAllButtonsEditable(self):
        states = [
                self.stateCallback_UpdateData_text(),
                self.stateCallback_EditButtonsAndColumns_text(),
                self.stateCallback_ImportExcel_text()
                ]
        return states
    def id_statecallbackToMakeAllButtonsEditable(self):
        list_ids = [
            self.submit_text_id,
            self.edit_button_text,
            self.import_excel_text_id
        ]
        return list_ids

    def outputStartEditateButtons(self):
        return False,False,False, True,True

    def outputEndEditateButtons(self):
        return True,True,True, False,False


class ReusableStandardButtons(ReusableSingleStandardButtons):
    def __init__(self, name_vue, StandardButtonsConfigSaver):
        super().__init__(name_vue, StandardButtonsConfigSaver)
        # self.ReusableInputs = reusable_inputs.ReusableInputs("-button-"+self.name_vue)
        # self.ReusableOutputs = reusable_outputs.ReusableOutputs("-button-"+self.name_vue)


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
        excel_input_div = html.Button(excel_input)
        return excel_input_div










