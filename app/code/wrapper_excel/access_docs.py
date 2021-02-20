# -*- coding: utf-8 -*-
from shutil import copyfile

import pandas as pd
import json




class AccessExcel():
    def __init__(self, ExcelPath):
        self.ExcelPath = ExcelPath
        self.useExampleIfNoImportedExcel()
    
    def useExampleIfNoImportedExcel(self):
        if self.ExcelPath.importedExcelExists():
            self.copyImportedExcel()
        else:
            self.copyExampleExcel()

    def copyImportedExcel(self):
        copyfile(self.ExcelPath.importedExcelPath(), self.ExcelPath.copiedExcelPath())

    def copyExampleExcel(self):
        copyfile(self.ExcelPath.exampleExcelPath(), self.ExcelPath.copiedExcelPath())
    
    def getDataframeOfExcel(self):
        path_excel = self.ExcelPath.copiedExcelPath()
        if '.csv' in path_excel:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif '.xlsx' in path_excel:
            # Assume that the user uploaded an excel file
            xl_file = pd.ExcelFile(path_excel)
        # elif '.xls' in filename:
            # Assume that the user uploaded an excel file
            # df = pd.read_excel(io.BytesIO(decoded))
            
        dfs = {sheet_name: xl_file.parse(sheet_name) 
                for sheet_name in xl_file.sheet_names}
        try:
            return dfs["Feuil1"]
        except KeyError:
            return dfs["Sheet1"]



class ExcelToDataframe():
    def __init__(self, ExcelPath):
        self.AccessExcel = AccessExcel(ExcelPath)
        self.updatDataframe()
        
    def getDataframe(self):
        return self._dfExcel
    
    def getDataframeAndEqCol(self):
        self.updatDataframe()
        equivalent_columns = self.getEquivalentColumns()
        dataframe = self.getDataframe()
        return dataframe, equivalent_columns
    
    def updatDataframe(self):
        dataframe = self.AccessExcel.getDataframeOfExcel()
        self._dfExcel = dataframe
    
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
    


class AccessTSTAuthorized():
    def __init__(self, ThemesAndSubthemesAuthorized):
        self.TSTAuth = ThemesAndSubthemesAuthorized
    
    def getJson(self):
        data = {}
        with open(self.TSTAuth.getTSTPath(), "r") as json_file:
            data = json.load(json_file)
        return data
    
    def updateJson(self, data):
        with open(self.TSTAuth.getTSTPath(), "w") as json_file:
            try:
                json.dump(data, json_file, indent=4)
            except TypeError:
                print("JSON of wrong type :\n", data)

    def getPrettyJson(self):
        data = self.getJson()
        json_formatted_str = json.dumps(data, indent=4) 
        return json_formatted_str
                
                
                
                