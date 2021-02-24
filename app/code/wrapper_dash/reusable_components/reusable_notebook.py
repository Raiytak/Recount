import dash_table

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd



class ReusableNotebook():
    def __init__(self, name_vue, ExcelToDataframe, ConfigNotebookExcelSaver):
        self.ExcelToDataframe = ExcelToDataframe
        self.ConfigNotebookExcelSaver = ConfigNotebookExcelSaver

        self.name_vue = name_vue
        self.notebook_name = self.name_vue+"notebook-excel"

    def getDataframe(self):
        dataframe =  self.ExcelToDataframe.getDataframeOfRawExcel()
        dataframe = self.changeFormatOfDataframe(dataframe)
        return dataframe

    def changeFormatOfDataframe(self, dataframe):
        try:
            dataframe["Date"] = pd.to_datetime(dataframe["Date"]).dt.strftime('%Y-%m-%d')
            return dataframe
        except Exception as e:
            print(" ->- Error reusable_notebbok -<- ")
            print(str(e))
            return dataframe

    def getData(self):
        dataframe = self.getDataframe()
        return self.getDataOfDataframe(dataframe)

    def getDataOfDataframe(self, dataframe):
        return dataframe.to_dict('records')


    def getConfigJson(self):
        return self.ConfigNotebookExcelSaver.getConfig()
        
    def getColumnsNameFromConfig(self):
        config_json = self.getConfigJson()
        column_names = config_json["columns_name"]
        return column_names

    def getDashNotebookDivFromDataframe(self, dataframe):
        columns_name = self.getColumnsNameFromConfig()
        notebook_excel_div = dash_table.DataTable(
            id=self.notebook_name,
            columns=[
                         {"name": columns_name[i], "id": i, "editable":False, "hideable":True, "renamable":True} if i == "ID"
                    else {"name": columns_name[i], "id": i, "type":"numeric", "hideable":True, "renamable":True} if (i == "Expense Euros" or i == "Expense Dollars" or i == "Sum Euros" or i == "Sum Dollars") 
                    else {"name": columns_name[i], "id": i, "type":"text", "hideable":True, "renamable":True} if (i == "Description" or i == "Category" or i == "Trip") 
                    else {"name": columns_name[i], "id": i, "type":"datetime", "hideable":True, "renamable":True} if i == "Date" 
                    else {"name": columns_name[i], "id": i, "hideable":True, "renamable":True}
                    for i in dataframe.columns],
            data=self.getData(),
            editable=True,

            # row_selectable="multi",
            row_deletable=True,

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


    def getDashNotebookCallbackAsStateData(self):
        return State(self.notebook_name, 'data')
    def getDashNotebookCallbackAsStateColumns(self):
        return State(self.notebook_name, 'columns')


