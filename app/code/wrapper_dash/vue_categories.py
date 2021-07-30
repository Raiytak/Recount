import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_outputs as reusable_outputs
import wrapper_dash.reusable_components.reusable_standard_buttons as reusable_standard_buttons
import wrapper_dash.reusable_components.reusable_links as reusable_links

import wrapper_dash.facilitator_dash.parser_json_to_html as parser_json_to_html


class ElementsVue():
    def __init__(self, accessAuthorizedTST, ReusableInputs, ReusableOutputs, ReusableStandardButtons, ParserJsonToHtml):
        self.accessAuthorizedTST = accessAuthorizedTST
        self.ReusableInputs = ReusableInputs
        self.ReusableOutputs = ReusableOutputs
        self.ReusableStandardButtons = ReusableStandardButtons
        self.ParserJsonToHtml = ParserJsonToHtml


    def getUpperVueDiv(self):
        update_div = self.ReusableStandardButtons.getUpdateDataDiv()
        edit_button = self.ReusableStandardButtons.getEditButtonsAndColumnsDiv()

        update_div_formated = html.Div(  
            children=[
                edit_button,
                update_div
                ],
            style={
                    "display":"flex",
                    "justify-content":"space-between"
                    }
            )


        return update_div_formated

    def getFullColumnStyle(self):
        style_returned = {
                        "display":"flex",
                        "flex-direction": "column",
                        # "width":"30%"
                    }
        return style_returned
    def getLittleLeftAndBiggerRightStyle(self):
        style_returned = {
                        "display":"flex",
                        "flex-direction": "row"
                    }
        return style_returned

    def getAddDivDiv(self, name_div, div_children='Add a layer'):
        add_div, add_div_id = self.ReusableInputs.getAddDivDiv(name_div, div_children)
        return add_div
    def getRemoveDivDiv(self, name_div, div_children='Remove a layer'):
        remove_div, remove_div_id = self.ReusableInputs.getRemoveDivDiv(name_div, div_children)
        return remove_div


    def getGroundZero(self):
        parsed_vue = self.ParserJsonToHtml.getEmbodyOfDict("root", self.accessAuthorizedTST.getTestJson(), 1)

        return parsed_vue




class EmptyVue():
    def __init__(self, accessAuthorizedTST, StandardButtonsConfigSaver):
        self.name_vue = "dashboard-home"

        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableOutputs = reusable_outputs.ReusableOutputs(self.name_vue)
        self.ReusableLinks = reusable_links.ReusableLinks()
        self.ReusableStandardButtons = reusable_standard_buttons.ReusableStandardButtons(self.name_vue, StandardButtonsConfigSaver)

        self.ParserJsonToHtml = parser_json_to_html.ParserJsonToHtml(self.ReusableInputs, self.ReusableOutputs)
        self.elementsVue = ElementsVue(accessAuthorizedTST, self.ReusableInputs, self.ReusableOutputs, self.ReusableStandardButtons, self.ParserJsonToHtml)
        
    def getEmptyVue(self):
        header_div = self.ReusableLinks.getHeaderSite()

        upper_div = self.elementsVue.getUpperVueDiv()   
        ground_zero = self.elementsVue.getGroundZero()     
        empty_vue = html.Div(
            children=[
                upper_div,
                ground_zero
            ]
        )

        total_vue = html.Div([
            header_div,
            empty_vue
        ])
        return total_vue





# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, accessAuthorizedTST, StandardButtonsConfigSaver):
        super().__init__(accessAuthorizedTST, StandardButtonsConfigSaver)
        self.app = app
        self.setCallback()
    
    def setCallback(self):
        @self.app.callback(
            Output('output_div', 'children'),
            [Input('submit-button', 'n_clicks')],
            [State('textarea-state', 'value')]
        )
        def update_categories(json_entered):     
            # print(json_entered)
            return ""


        @self.app.callback(
            self.ReusableStandardButtons.EditButtons.outputcallbacks_categories(),
            self.ReusableStandardButtons.EditButtons.inputcallbacks_categories(),
            self.ReusableStandardButtons.EditButtons.statecallbacks_categories()
            )
        def edit_buttons_categories(check_value):  
            texts_to_save = []
            list_ids = self.ReusableStandardButtons.EditButtons.id_statecallbacks_categories()

            return self.ReusableStandardButtons.EditButtons.edit_buttons_categories(check_value, list_ids, texts_to_save)
        
        # @self.app.callback(
        #     self.ReusableStandardButtons.UpdateButton.outputcallbacks(),
        #     self.ReusableStandardButtons.UpdateButton.inputcallbacks()
        #     )
        # def do_update(n_clicks_submit, data_notebook, columns_notebook):
        #     message_to_user = "Helloo"
        #     return message_to_user

    def setThisVue(self):
        return self.getEmptyVue()


    
