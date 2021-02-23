import dash_table

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State



class ReusableNotebook():
    def __init__(self, name_vue, ExcelToDataframe):
        self.ExcelToDataframe = ExcelToDataframe

        self.name_vue = name_vue
        self.notebook_name = self.name_vue+"notebook-excel"

    def getDataframe(self):
        return self.ExcelToDataframe.getDataframeOfRawExcel()

    def getData(self):
        dataframe = self.getDataframe()
        return self.getDataOfDataframe(dataframe)

    def getDataOfDataframe(self, dataframe):
        return dataframe.to_dict('records')

    def getDashNotebookDivFromDataframe(self, dataframe):
        notebook_excel_div = dash_table.DataTable(
            id=self.notebook_name,
            columns=[
                    {"name": i, "id": i, "editable":False} if i == "ID"
                    else {"name": i, "id": i, "type":"numeric"} if (i == "Expense Euros" or i == "Expense Dollars" or i == "Sum Euros" or i == "Sum Dollars") 
                    else {"name": i, "id": i, "type":"text"} if (i == "Description" or i == "Category" or i == "Trip") 
                    else {"name": i, "id": i, "type":"datetime"} if i == "Date" 
                    else {"name": i, "id": i}
                    for i in dataframe.columns],
            data=self.getData(),
            editable=True,

            export_columns='all',
            export_format='xlsx',
            export_headers='display',
        )
        return notebook_excel_div

    def getDashNotebookDiv(self):
        dataframe = self.getDataframe()
        notebook_excel_div = self.getDashNotebookDivFromDataframe(dataframe)
        return notebook_excel_div

    def getDashNotebookCallback(self):
        return Input(self.notebook_name, 'data')

    def getDashNotebookCallbackAsOutput(self):
        return Output(self.notebook_name, 'data')