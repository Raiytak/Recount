# -*- coding: utf-8 -*-

# === DESCRIPTION ===
# This file aims to do the CRUD manipulations on the files used by the application.
# The paths used are stored in the paths_docs module, and are used by the wrappers of this module.


import pandas as pd




# This class load the copy_expenses.xmlx file in code/data and converts it to a dataframe used by other functions
class ExcelToDataframe():
    def __init__(self, AccessExcel):
        self.AccessExcel = AccessExcel
        self.ExcelPath = self.AccessExcel.ExcelPath
        
    def getDataframeOf(self, path_excel):
        xl_file = pd.ExcelFile(path_excel)
        dfs = {sheet_name: xl_file.parse(sheet_name) 
                for sheet_name in xl_file.sheet_names}
        try:
            return dfs["Feuil1"]
        except KeyError:
            return dfs["Sheet1"]

    def getDataframeOfExcel(self):
        path_excel = self.ExcelPath.copiedExcelPath()
        return self.getDataframeOf(path_excel)
    def getDataframe(self):
        return self.getDataframeOfExcel()

    def getDataframeOfRawExcel(self):
        path_excel = self.ExcelPath.rawCopiedExcelPath()
        return self.getDataframeOf(path_excel)
    def getDataframeOfExampleExcel(self):
        path_excel = self.ExcelPath.exampleExcelPath()
        return self.getDataframeOf(path_excel)
    
    def getDataframeAndEqCol(self):
        equivalent_columns = self.getEquivalentColumns()
        dataframe = self.getDataframe()
        return dataframe, equivalent_columns
    
    
    # This works like this :
    #   - "column excel" : ["column sql"]
    def getEquivalentColumns(self):
        equivalent_columns = {"ID":["ID"], "Date":["date"], "Expenses":["amount"],
                            "Category":["category"], "Theme":["theme"],
                            "Trip":["trip"], "Type":["payment_method"],
                            "Company":["company"], "Description":["description"]}
        return  equivalent_columns
            
            
                