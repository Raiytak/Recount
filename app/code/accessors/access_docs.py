# -*- coding: utf-8 -*-

# === DESCRIPTION ===
# This file aims to do the CRUD manipulations on the files used by the application.
# The paths used are stored in the paths_docs module, and are used by the wrappers of this module.

from shutil import copyfile

import pandas as pd
import json

import os




class AccessExcel():
    def __init__(self, ExcelPath):
        self.ExcelPath = ExcelPath
        self.cleanOldExcels()
        self.useExampleIfNoImportedExcel()

        self.removeAllOldFiles()
    
    def useExampleIfNoImportedExcel(self):
        if self.ExcelPath.importedExcelExists():
            self.copyImportedExcel()
        else:
            self.copyExampleExcel()

    def copyImportedExcel(self):
        copyfile(self.ExcelPath.importedExcelPath(), self.ExcelPath.copiedExcelPath())
        copyfile(self.ExcelPath.importedExcelPath(), self.ExcelPath.rawCopiedExcelPath())
    def copyExampleExcel(self):
        copyfile(self.ExcelPath.exampleExcelPath(), self.ExcelPath.copiedExcelPath())
        copyfile(self.ExcelPath.exampleExcelPath(), self.ExcelPath.rawCopiedExcelPath())


    def removeFile(self, path_file):
        try:
            os.remove(path_file)
        except FileNotFoundError:
            pass
    def removeCopiedExcel(self):
        self.removeFile(self.ExcelPath.copiedExcelPath())
    def removeImportedExcel(self):
        self.removeFile(self.ExcelPath.importedExcelPath())
    def removeAllOldFiles(self):
        if self.ExcelPath.importedExcelExists() == True:
            self.removeImportedExcel()
        if self.ExcelPath.copiedExcelPath() == True:
            self.removeCopiedExcel()
    
    def cleanOldExcels(self):
        self.removeCopiedExcel()


    # def getDataframeOfImportedExcel(self):
    #     if self.ExcelPath.importedExcelExists() == True:
    #         path_excel = self.ExcelPath.importedExcelPath()
    #         return self.getDataframeOf(path_excel)
    #     else:
    #         return self.getDataframeOfRawExcel()

    def updateExcel(self):
        if self.ExcelPath.importedExcelExists() == True:
            self.copyImportedExcel()


# This class load the copy_expenses.xmlx file in code/data and converts it to a dataframe used by other functions
class ExcelToDataframe():
    def __init__(self, ExcelPath):
        self.AccessExcel = AccessExcel(ExcelPath)
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
        self.AccessExcel.updateExcel()
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
    def getDataframeOfImportedFile(self):
        return self.getDataframeOf(self.AccessExcel.ExcelPath.importedExcelPath())
    
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
            
            

class AccessDescrToTheme():
    def __init__(self, DescrToThemePath):
        self.DescrToThemePath = DescrToThemePath
        
    def getJsonDescrToTheme(self):
        data = {}
        try:
            with open(self.DescrToThemePath.getDescriptionToThemePath(), "r") as json_file:
                data = json.load(json_file)
        # Case where the document isn't created yet
        except FileNotFoundError:
            self.updateDescrConvJson(data)

        return data
    
    def updateDescrConvJson(self, data):
        with open(self.DescrToThemePath.getDescriptionToThemePath(), "w") as json_file:
            try:
                json.dump(data, json_file)
            except TypeError:
                print("JSON of wrong type :\n", data)
    


class AccessCTAuthorized():
    def __init__(self, CategoryAndThemeAuthorized):
        self.TSTAuth = CategoryAndThemeAuthorized
    
    def getJson(self):
        data = {}
        with open(self.TSTAuth.getCategoryAndThemePath(), "r") as json_file:
            data = json.load(json_file)
        return data
    
    def updateJson(self, data):
        with open(self.TSTAuth.getCategoryAndThemePath(), "w") as json_file:
            try:
                json.dump(data, json_file, indent=4)
            except TypeError:
                print("JSON of wrong type :\n", data)

    def getPrettyJson(self):
        data = self.getJson()
        json_formatted_str = json.dumps(data, indent=4) 
        return json_formatted_str
                
                
                
                