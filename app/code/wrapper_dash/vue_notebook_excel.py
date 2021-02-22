import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


import datetime


import wrapper_dash.reusable_components.reusable_inputs as reusable_inputs
import wrapper_dash.notebook_excel.convert_df_to_dash_components as convert_df_to_dash_components




class ElementsVue():
    def __init__(self, ExcelToDataframe, ReusableInputs):
        self.ReusableInputs = ReusableInputs
        self.ExcelToDataframe = ExcelToDataframe
        self.ConverterDfToDash = convert_df_to_dash_components.ConverterDfToDash(self.ExcelToDataframe)

    def getInputDiv(self):
        return self.ReusableInputs.getDatePeriodAndExcelDiv()
    def getInputCallbacks(self):
        return self.ReusableInputs.getDatePeriodAndExcelCallbacks()

    def getEmptyExcelNotebook(self):
        notebook_excel = self.ConverterDfToDash.getDashNotebook()
        notebook_excel_div = html.Div(id="notebook-excel", children=notebook_excel)
        return notebook_excel_div


    def getOutputDiv(self):
        output_div = html.Div(id="output-div")
        return output_div
        



class EmptyVue():
    def __init__(self, ExcelToDataframe):
        self.name_vue = "notebook-excel-"
        self.ReusableInputs = reusable_inputs.ReusableInputs(self.name_vue)
        self.elementsVue = ElementsVue(ExcelToDataframe, self.ReusableInputs)

        
    def getEmptyVue(self):
        input_div = self.elementsVue.getInputDiv()
        output_div = self.elementsVue.getOutputDiv()
        excel_notebook = self.elementsVue.getEmptyExcelNotebook()

        total_vue = html.Div([input_div, output_div, excel_notebook])
        return total_vue


    def getInputCallbacks(self):
        return self.elementsVue.getInputCallbacks()





# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app, ExcelToDataframe):
        super().__init__(ExcelToDataframe)
        self.app = app
        self.ExcelToDataframe = ExcelToDataframe

        self.setCallback()
    
    def setCallback(self):
        @self.app.callback(
            Output("output-div", "value"),
            self.getInputCallbacks())
        def update_of_notebook(selected_date_str, selected_periode, imported_file):     
             
            
            return ""

    def setThisVue(self):
        return self.getEmptyVue()


    
