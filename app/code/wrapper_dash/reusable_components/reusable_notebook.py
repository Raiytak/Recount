import dash_table

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import wrapper_dash.reusable_components.reusable_links as reusable_links

import pandas as pd


class FunctionsForReusableNotebook():
    def __init__(self, name_vue, ExcelToDataframe, ConfigNotebookExcelSaver, ReusableStandardButtons):
        self.name_vue = name_vue
        self.notebook_name = self.name_vue+"notebook-excel"

        self.ExcelToDataframe = ExcelToDataframe
        self.ConfigNotebookExcelSaver = ConfigNotebookExcelSaver

        self.ReusableStandardButtons = ReusableStandardButtons
        self.EditButtons = self.ReusableStandardButtons.EditButtons




    def addRowInTheNotebookData(self, data_notebook, columns_notebook):
        next_id = data_notebook[-1]["ID"]+1
        data_notebook.append({
            c['id']:('' if c['id'] != "ID" else next_id)
            for c in columns_notebook
            })
        message_to_user = "row added" 
        data_for_output = data_notebook

        return message_to_user, data_for_output




    def changeFormatOfDataframe(self, dataframe):
        try:
            dataframe["Date"] = pd.to_datetime(dataframe["Date"]).dt.strftime('%Y-%m-%d')
            return dataframe
        except Exception as e:
            print(e)
            return dataframe

    def getDataframe(self):
        dataframe =  self.ExcelToDataframe.getDataframeOfRawExcel()
        dataframe = self.changeFormatOfDataframe(dataframe)
        return dataframe

    def translateDataframeToNotebookData(self, dataframe):
        data_for_output = dataframe.to_dict('records')
        return data_for_output

    def getNotebookData(self):
        dataframe = self.getDataframe()
        data_for_output = self.translateDataframeToNotebookData(dataframe)
        return data_for_output



    def getConfigJson(self):
        return self.ConfigNotebookExcelSaver.getConfig()
        
    def getColumnsNameFromConfig(self):
        config_json = self.getConfigJson()
        column_names = config_json["columns_name"]
        return column_names





class ReusableSingleElementsNotebook(FunctionsForReusableNotebook):
    def __init__(self, name_vue, ExcelToDataframe, ConfigNotebookExcelSaver, ReusableStandardButtons):
        super().__init__(name_vue, ExcelToDataframe, ConfigNotebookExcelSaver, ReusableStandardButtons)
        self.add_row_button = self.name_vue + 'add-rows-button'
        self.add_row_button_message = self.add_row_button + '-message'



    def getAddRowButton(self):
        return html.Button('Add Row', id=self.add_row_button, n_clicks=0)
    def inputcallback_AddRow_n_clicks(self):
        return Input(self.add_row_button, 'n_clicks')

    def getAddRowMessageDiv(self):
        add_row_message = html.Div(
            id=self.add_row_button_message,
            )
        return add_row_message
    def outputcallback_AddRowMessage_style(self):
        return Output(self.add_row_button_message, 'style')

    def getAddRowDiv(self):
        add_row_div_total = html.Div(
            children=[
                self.getAddRowButton(),
                self.getAddRowMessageDiv()
            ]
        )
        return add_row_div_total


    def getNotebookDiv(self):
        notebook_excel = self.getDashNotebookDiv()
        notebook_excel_div = html.Div(id="notebook-excel", children=notebook_excel)
        return notebook_excel_div





    def getDashNotebookDivFromDataframe(self, dataframe):
        columns_name = self.getColumnsNameFromConfig()
        notebook_excel_div = dash_table.DataTable(
            id=self.notebook_name,
            columns=[
                         {"name": columns_name[i], "id": i, "editable":False, "hideable":True, "renamable":True} if i == "ID"
                    else {"name": columns_name[i], "id": i, "type":"numeric", "hideable":True, "renamable":True} if (i == "Expense Euros" or i == "Expense Dollars") 
                    else {"name": columns_name[i], "id": i, "type":"text", "hideable":True, "renamable":True} if (i == "Description" or i == "Category" or i == "Trip") 
                    else {"name": columns_name[i], "id": i, "type":"datetime", "hideable":True, "renamable":True} if i == "Date" 
                    else {"name": columns_name[i], "id": i, "hideable":True, "renamable":True}
                    for i in dataframe.columns],
            data=self.getNotebookData(),
            editable=True,

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





    def outputcallback_Notebook_data(self):
        return Output(self.notebook_name, 'data')

    def statecallback_Notebook_data(self):
        return State(self.notebook_name, 'data')
    def statecallback_Notebook_columns(self):
        return State(self.notebook_name, 'columns')





class ReusableNotebook(ReusableSingleElementsNotebook):
    def __init__(self, name_vue, ExcelToDataframe, ConfigNotebookExcelSaver, ReusableStandardButtons):
        super().__init__(name_vue, ExcelToDataframe, ConfigNotebookExcelSaver, ReusableStandardButtons)
        self.AddRow = AddRow(self)
        self.ReusableLinks = reusable_links.ReusableLinks()

    def getUpperVueDiv(self):
        update_div = self.ReusableStandardButtons.getUpdateDataDiv()
        edit_button = self.ReusableStandardButtons.getEditButtonsAndColumnsDiv()
        import_excel = self.ReusableStandardButtons.getImportExcelDiv()

        update_div_formated = html.Div(  
            children=[
                edit_button,
                update_div,
                import_excel
                ],
            style={
                    "display":"flex",
                    "justify-content":"space-between"
                    }
            )


        return update_div_formated



    def getEmptyVue(self):
        header_div = self.ReusableLinks.getHeaderSite()

        input_div = self.getUpperVueDiv()
        excel_notebook = self.getNotebookDiv()
        add_row_div = self.getAddRowDiv()
        content_div = html.Div([input_div, excel_notebook, add_row_div])

        total_vue = html.Div([header_div, content_div])
        return total_vue




class AddRow():
    def __init__(self, ReusableNotebook):        
        self.ReusableNotebook = ReusableNotebook


    # Part to do the actions on check/uncheck of the checkbox
    def outputcallbacks(self):
        list_outputs = [
            self.ReusableNotebook.outputcallback_AddRowMessage_style(),
            self.ReusableNotebook.outputcallback_Notebook_data()
            ]
        return list_outputs
    def inputcallbacks(self):
        return self.ReusableNotebook.inputcallback_AddRow_n_clicks()
    def statecallbacks(self):
        list_states = [
            self.ReusableNotebook.statecallback_Notebook_data(),
            self.ReusableNotebook.statecallback_Notebook_columns()
        ]
        return list_states

    def add_row_notebook(self, data_notebook, columns_notebook):   
        return self.ReusableNotebook.addRowInTheNotebookData(data_notebook, columns_notebook)