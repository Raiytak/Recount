# -*- coding: utf-8 -*-
from shutil import copyfile
import json

import pandas as pd


class DataPath():
    def getDataPath(self):
        path_data = r"C:\Users\User1\Desktop\Projets\Comptes\data"
        return path_data

    def popEnd(self, name_directory):
        size = len(name_directory)
        for i in range(size-1,0,-1):
            if name_directory[i] == "/":
                break
        return name_directory[0:i]



class ExcelPath(DataPath):
    def __init__(self):
        self.excel_path = self.getProjectExcelPath()
        self._real_excel_path = self.getRealExcelPath()
    
    def getProjectExcelPath(self):
        project_excelexcel = self.getDataPath() + "/comptes.xlsx"
        return project_excelexcel
        
    def getRealExcelPath(self):
        path_excel = r"C:\Users\User1\Desktop\Le Dossier\Comptes\credit_etudiant.xlsx"
        return path_excel



class DescrToThemePath(DataPath):        
    def getDescriptionToThemePath(self):
        path_conv = self.getDataPath() + "/convert_descr_to_theme.json"
        return path_conv
    


class ThemesAndSubthemesAuthorized(DataPath):        
    def getTSTPath(self):
        path_conv = self.getDataPath() + "/themes_subthemes_authorized.json"
        return path_conv
    

