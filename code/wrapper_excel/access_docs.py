# -*- coding: utf-8 -*-
from shutil import copyfile

import pandas as pd
import json




class AccessExcel():
    def __init__(self, ExcelPath):
        self.ExcelPaths = ExcelPath
        self.useExampleIfNoImportedExcel()
    
    def useExampleIfNoImportedExcel(self):
        if self.ExcelPaths.importedExcelExists():
            self.copyImportedExcel()
        else:
            self.copyExampleExcel()

    def copyImportedExcel(self):
        copyfile(self.ExcelPaths.importedExcelPath(), self.ExcelPaths.copiedExcelPath())

    def copyExampleExcel(self):
        copyfile(self.ExcelPaths.exampleExcelPath(), self.ExcelPaths.copiedExcelPath())
    
    def getDataframeOfExcel(self):
        filename = self.ExcelPaths.copiedExcelPath()
        if '.csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif '.xlsx' in filename:
            # Assume that the user uploaded an excel file
            xl_file = pd.ExcelFile(self.ExcelPaths.copiedExcelPath())
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
        
    def getEquivalentColumns(self):
        equivalent_columns = {"ID":["ID"], "Date":["date"], "Dépenses":["montant"],
                            "Theme":["theme"], "Soustheme":["soustheme"],
                            "Voyage":["voyage"], "Type":["methode_payement"],
                            "Entreprise":["entreprise"], "Description":["description"]}
        return  equivalent_columns
            
            

class AccessDescrToTheme():
    def __init__(self, DescrToThemePath):
        self.DescrToThemePath = DescrToThemePath
        
    def getJsonDescrToTheme(self):
        data = {}
        with open(self.DescrToThemePath.getDescriptionToThemePath(), "r") as json_file:
            data = json.load(json_file)
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
                json.dump(data, json_file)
            except TypeError:
                print("JSON of wrong type :\n", data)
                
                
                
                