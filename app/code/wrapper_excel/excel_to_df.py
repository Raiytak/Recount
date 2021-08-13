# -*- coding: utf-8 -*-

# === DESCRIPTION ===
# This file aims to do the CRUD manipulations on the files used by the application.
# The paths used are stored in the paths_docs module, and are used by the wrappers of this module.


import pandas as pd

from accessors.access_files import AccessExcel, AccessUserFiles


# This class load the copy_expenses.xmlx file in code/data and converts it to a dataframe used by other functions
class ExcelToDataframe:
    def __init__(self, username=""):
        if username != "":
            self.AccessUserFiles = AccessUserFiles(username)
            self.AccessExcel = self.AccessUserFiles.AccessExcel
        else:
            self.AccessUserFiles = None
            self.AccessExcel = AccessExcel()
        self.ExcelPaths = self.AccessExcel.ExcelPaths

    def getDataframeOf(self, path_excel):
        xl_file = pd.ExcelFile(path_excel)
        dfs = {
            sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names
        }
        try:
            dataframe = dfs["Feuil1"]
        except KeyError:
            try:
                dataframe = dfs["Sheet1"]
            except KeyError:
                raise Exception
        list_columns = dataframe.columns
        for column_name in list_columns:
            if "Unnamed" in column_name:
                dataframe = dataframe.drop(columns=column_name)
        return dataframe

    def getDataframeOfExcel(self):
        path_excel = self.ExcelPaths.cleanedExcelPath()
        return self.getDataframeOf(path_excel)

    def getDataframe(self):
        return self.getDataframeOfExcel()

    def getDataframeOfRawExcel(self):
        path_excel = self.ExcelPaths.rawExcelPath()
        return self.getDataframeOf(path_excel)

    def getDataframeOfExampleExcel(self):
        path_excel = self.ExcelPaths.exampleExcelPath()
        return self.getDataframeOf(path_excel)

    def getDataframeAndEqCol(self):
        equivalent_columns = self.getEquivalentColumns()
        dataframe = self.getDataframe()
        return dataframe, equivalent_columns

    # This works like this :
    #   - "column excel" : ["column sql"]
    def getEquivalentColumns(self):
        equivalent_columns = {
            "username": ["username"],
            "ID": ["ID"],
            "Date": ["date"],
            "Expenses": ["amount"],
            "Category": ["category"],
            "Theme": ["theme"],
            "Trip": ["trip"],
            "Type": ["payment_method"],
            "Company": ["company"],
            "Description": ["description"],
        }
        return equivalent_columns
