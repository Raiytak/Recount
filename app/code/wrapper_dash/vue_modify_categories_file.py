import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_outputs as reusable_outputs

import wrapper_dash.facilitator_dash.parser_json_to_html as parser_json_to_html


class ElementsVue():
    def __init__(self, accessAuthorizedTST, ReusableInputs, ReusableOutputs, ParserJsonToHtml):
        self.accessAuthorizedTST = accessAuthorizedTST
        self.ReusableInputs = ReusableInputs
        self.ReusableOutputs = ReusableOutputs
        self.ParserJsonToHtml = ParserJsonToHtml

    def getTextAreaDiv(self):
        text_area = dcc.Textarea(
            id='textarea-state',
            value=self.accessAuthorizedTST.getPrettyJson(),
            style={'width': '60%', 'height': 200},
            )

        # my_button = html.Div('Import csv File')
        submit_button = html.Button('Submit', id='submit-button', n_clicks=0)

        output_div = html.Div(id='output_div', style={'whiteSpace': 'pre-line'})

        input_div = html.Div(  children=[text_area, submit_button, output_div],
                                    # style={
                                    #     "display":"column",
                                    #     "justify-content":"space-between"}
                                        )

        return text_area        

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
        ground_zero = 'ground-zero'
        h1_div, h1_div_id = self.ReusableOutputs.getH1Div(ground_zero)
        h2_div, h2_div_id = self.ReusableOutputs.getH2Div(ground_zero)
        h3_div, h3_div_id = self.ReusableOutputs.getH3Div(ground_zero)
        h4_div, h4_div_id = self.ReusableOutputs.getH4Div(ground_zero)

        h3_toolkit = html.Div(
            children=[
                h3_div,
                self.getAddDivDiv(ground_zero+'-h3-', '+'),
                self.getRemoveDivDiv(ground_zero+'-h3-', '-')
            ],
            style=self.getFullColumnStyle()
        )
        h3_embody = html.Div(
            children=[
                h3_toolkit,
                h4_div
            ],
            style=self.getLittleLeftAndBiggerRightStyle()
        )

        h2_toolkit = html.Div(
            children=[
                h2_div,
                self.getAddDivDiv(ground_zero+'-h2-', '+'),
                self.getRemoveDivDiv(ground_zero+'-h2-', '-')
            ],
            style=self.getFullColumnStyle()
        )
        h2_embody = html.Div(
            children=[
                h2_toolkit,
                h3_embody
            ],
            style=self.getLittleLeftAndBiggerRightStyle()
        )

        h1_toolkit = html.Div(
            children=[
                h1_div,
                self.getAddDivDiv(ground_zero+'-h1-'),
                self.getRemoveDivDiv(ground_zero+'-h1-')
            ],
            style=self.getFullColumnStyle()
        )
        h1_embody = html.Div(
            children=[
                h1_toolkit,
                h2_embody
            ],
            style=self.getLittleLeftAndBiggerRightStyle()
        )

        global_vue = h1_embody



        parsed_vue = self.ParserJsonToHtml.getEmbodyOfDict("root", self.accessAuthorizedTST.getTestJson(), 1)



        return parsed_vue




class EmptyVue():
    def __init__(self, accessAuthorizedTST):
        self.name_vue = "dashboard-home-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableOutputs = reusable_outputs.ReusableOutputs(self.name_vue)
        self.ParserJsonToHtml = parser_json_to_html.ParserJsonToHtml(self.ReusableInputs, self.ReusableOutputs)
        self.elementsVue = ElementsVue(accessAuthorizedTST, self.ReusableInputs, self.ReusableOutputs, self.ParserJsonToHtml)
        
    def getEmptyVue(self):
        text_area_div = self.elementsVue.getTextAreaDiv()   
        ground_zero = self.elementsVue.getGroundZero()     
        empty_vue = html.Div(
            children=[
                text_area_div,
                ground_zero
            ]
        )
        return empty_vue





# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, accessAuthorizedTST):
        super().__init__(accessAuthorizedTST)
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

    def setThisVue(self):
        return self.getEmptyVue()


    
