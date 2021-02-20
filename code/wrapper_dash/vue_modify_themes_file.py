import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import datetime



class ElementsVue():
    def __init__(self, accessAuthorizedTST):
        self.accessAuthorizedTST = accessAuthorizedTST

    def getInputDiv(self):
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



class EmptyVue():
    def __init__(self, accessAuthorizedTST):
        self.elementsVue = ElementsVue(accessAuthorizedTST)
        
    def getEmptyVue(self):
        input_div = self.elementsVue.getInputDiv()        
        return input_div





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
        def update_themes(json_entered):     
            # print(json_entered)
            return ""

    def setThisVue(self):
        return self.getEmptyVue()


    
