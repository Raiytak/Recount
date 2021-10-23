# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This file aims to do the CRUD manipulations on the excel files used by the application.
The paths used are stored in the paths_docs module, and are used by the wrappers of this module.
"""

from logging import root
import pandas as pd
from pymysql import NULL

from accessors.access_files import AccessExcel, AccessUserFiles
from accessors.data_encryption import ExcelEncryption


class ExcelToDataframe:
    """Wrapper to get the user data from its excel, and the SQL equivalent columns"""

    def __init__(self, username=""):
        if username != "":
            self.AccessUserFiles = AccessUserFiles(username)
            self.AccessExcel = self.AccessUserFiles.AccessExcel
        else:
            self.AccessUserFiles = None
            self.AccessExcel = AccessExcel()
        self.ExcelPaths = self.AccessExcel.ExcelPaths
        self.ExcelEncryption = ExcelEncryption()

    def getDataframeOf(self, path_excel):
        excel_data = self.ExcelEncryption.getDataFrom(path_excel)
        try:
            dataframe = pd.read_excel(excel_data)
        except TypeError:
            # TODO : notify and show error to user
            dataframe = self.getDataframeOf(
                self.AccessExcel.ExcelPaths.exampleExcelPath()
            )
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
