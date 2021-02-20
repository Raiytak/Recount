import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import wrapper_dash.vue_links_other_vues as vue_links_other_vues



class ElementsVue():
    def __init__(self):
        pass

    def getDefaultInputDiv(self):
        location = dcc.Location(id='default-url', refresh=False)
        page_content = html.Div(id='default-page-content')
        default_input_div = html.Div( children=[location, page_content])
        return default_input_div        

    def getInputDiv(self):
        location = dcc.Location(id='url', refresh=False)
        page_content = html.Div(id='page-content')
        input_div = html.Div( children=[location, page_content])
                                    # style={
                                    #     "display":"column",
                                    #     "justify-content":"space-between"}
                                        # )
        return input_div        

    def getLinksDiv(self):
        return vue_links_other_vues.getLinksDiv()


class EmptyVue():
    def __init__(self):
        self.elementsVue = ElementsVue()
        
    def getEmptyDefaultVue(self):
        elem_input_div = self.elementsVue.getDefaultInputDiv()  
        all_the_vue = html.Div(elem_input_div)   
        return all_the_vue

    def getEmptyVue(self):
        elem_input_div = self.elementsVue.getInputDiv()  
        elem_links_div = self.elementsVue.getLinksDiv()  
        all_the_vue = html.Div([elem_links_div, elem_input_div])   
        return all_the_vue





# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app
        # self.setCallback()
    
    # def setCallback(self):
    #     @self.app.callback(
    #     )
    #     def update_themes(json_entered):   
    def setThisEmptyDefaultVue(self):
        return self.getEmptyDefaultVue()

    def setThisVue(self):
        return self.getEmptyVue()


    
