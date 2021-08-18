import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from wrapper_dash.reusable_components.reusable_inputs import ReusableInputs
from wrapper_dash.reusable_components.reusable_outputs import ReusableOutputs
from wrapper_dash.reusable_components.reusable_links import ReusableLinks

import wrapper_dash.facilitator_dash.user_identification as user_identification
import wrapper_dash.facilitator_dash.tools as tools

from accessors.access_files import AccessUserFiles

import update_data


class ElementsVue:
    def __init__(self, ReusableInputs, ReusableOutputs, ReusableLinks):
        self.ReusableInputs = ReusableInputs
        self.ReusableOutputs = ReusableOutputs
        self.ReusableLinks = ReusableLinks

    def getResetUserData(self):
        return self.ReusableInputs.getResetUserData()

    def getResetUserDataCallback(self):
        return self.ReusableInputs.getResetUserDataCallback()

    def getConfirmDialogueInputCallback(self):
        output_conf, input_conf = self.ReusableOutputs.getConfirmDialogueCallbacks()
        return input_conf

    def getConfirmDialogueOutputCallback(self):
        output_conf, input_conf = self.ReusableOutputs.getConfirmDialogueCallbacks()
        return output_conf


class EmptyVue:
    def __init__(self):
        self.name_vue = "home-page-"
        self.ReusableInputs = ReusableInputs(self.name_vue)
        self.ReusableOutputs = ReusableOutputs(self.name_vue)
        self.ReusableLinks = ReusableLinks()
        self.ElementsVue = ElementsVue(
            self.ReusableInputs, self.ReusableOutputs, self.ReusableLinks
        )

    def getEmptyVue(self):
        reset_button = self.ElementsVue.getResetUserData()
        conf_dial = self.ReusableOutputs.getConfirmDialogue()
        hidden_vue = self.ReusableOutputs.getHiddenDiv("reset-button")
        all_the_vue = html.Div([reset_button, conf_dial, hidden_vue])
        return all_the_vue

    def getConfirmDialogueOutputCallback(self):
        return self.ElementsVue.getConfirmDialogueOutputCallback()

    def getResetExportConfirmInputCallback(self):
        return self.ElementsVue.getConfirmDialogueInputCallback()

    def getResetCallback(self):
        return self.ElementsVue.getResetUserDataCallback()


# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setCallback()

    def setCallback(self):
        @self.app.callback(
            self.getConfirmDialogueOutputCallback(), self.getResetCallback()
        )
        def reset_data(reset_nclicks):
            id_component_called = tools.getIdButtonClicked()
            if "reset" in id_component_called:
                return True
            return False

        @self.app.callback(
            self.ReusableOutputs.getHiddenDivCallback("reset-button"),
            self.getResetExportConfirmInputCallback(),
        )
        def confirm_reset(conf_dial_submited):
            username = user_identification.getUsername()
            myAccessUserFiles = AccessUserFiles(username)

            if conf_dial_submited != None:
                myAccessUserFiles.removeExcelsOfUser()
                update_data.removeAllDataForUser(username)
            return ""

    def setThisVue(self):
        return self.getEmptyVue()
