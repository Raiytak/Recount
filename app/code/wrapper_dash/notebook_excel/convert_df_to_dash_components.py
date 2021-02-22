import dash_table



class ConverterDfToDash():
    def __init__(self, ExcelToDataframe):
        self.ExcelToDataframe = ExcelToDataframe

    def getDataframe(self):
        return self.ExcelToDataframe.getDataframe()

    def getDashNotebook(self):
        dataframe = self.getDataframe()
        notebook_excel_div = dash_table.DataTable(
            id='table',
            columns=[
                    {"name": i, "id": i, "editable":False} if i == "ID"
                    else {"name": i, "id": i, "type":"numeric"} if (i == "Expense Euros" or i == "Expense Dollars" or i == "Sum Euros" or i == "Sum Dollars") 
                    else {"name": i, "id": i, "type":"text"} if (i == "Description" or i == "Category" or i == "Trip") 
                    else {"name": i, "id": i, "type":"datetime"} if i == "Date" 
                    else {"name": i, "id": i}
                    for i in dataframe.columns],
            data=dataframe.to_dict('records'),
            editable=True,
        )
        return notebook_excel_div
