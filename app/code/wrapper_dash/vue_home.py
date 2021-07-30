import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.reusable_components.reusable_links as reusable_links


class ElementsVue():
    def __init__(self, ReusableInputs, ReusableLinks):
        self.ReusableInputs = ReusableInputs
        self.ReusableLinks = ReusableLinks
        

    def getHeader(self):
        return self.ReusableLinks.getHeaderSite()



class EmptyVue():
    def __init__(self):
        self.name_vue = "home-page-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.ReusableLinks = reusable_links.ReusableLinks()
        self.elementsVue = ElementsVue(self.ReusableInputs, self.ReusableLinks)
        
    def getEmptyVue(self):
        header_div = self.elementsVue.getHeader()  

        all_the_vue = html.Div([header_div])   
        return all_the_vue

    def getInputCallbacks(self):
        return self.ReusableInputs.getLocationCallback()




# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setCallback()
    
    def setCallback(self):
        pass

    def setThisVue(self):
        return self.getEmptyVue()


    
