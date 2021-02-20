import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import wrapper_dash.vue_links_other_vues as vue_links_other_vues


class ElementsVue():
    def __init__(self):
        pass


    def getInputDiv(self):
        location = dcc.Location(id='url-home', refresh=False)

        page_content = html.Div(id='page-content-home')

        input_div = html.Div( children=[location, page_content])
                                    # style={
                                    #     "display":"column",
                                    #     "justify-content":"space-between"}
                                        # )
        return input_div        

    def getLinksDiv(self):
        return vue_links_other_vues.getLinksDiv()

    def getTextDiv(self):
        link_page_dashhome = dcc.Link('Go to Page Dashboard Home', href='/dashhome')
        link_page_home = dcc.Link('Go to Page Home', href='/home')
        link_page_themes = dcc.Link('Go to Page Themes', href='/themes')

        links_div = html.Div(children=[link_page_home, link_page_dashhome, link_page_themes],
                                    style={
                                        "display":"flex",
                                        "justify-content":"space-between"}
                                        )
        return links_div

    def getOtherTextArea(self):
        return ''



class EmptyVue():
    def __init__(self):
        self.elementsVue = ElementsVue()
        
    def getEmptyVue(self):
        elem_input_div = self.elementsVue.getInputDiv()  
        elem_links_div = self.elementsVue.getLinksDiv()     
        all_the_vue = html.Div([elem_input_div, elem_links_div])   
        return all_the_vue





# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setCallback()
    
    def setCallback(self):
        @self.app.callback(
            Output('page-content-home', 'children'),
            Input("url-home", 'pathname'))
        def display_home(pathname):     
            return ''

    def setThisVue(self):
        return self.getEmptyVue()


    
