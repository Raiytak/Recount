# -*- coding: utf-8 -*-
from shutil import copyfile
import json

import pandas as pd

import getpass


username = getpass.getuser()
MAIN_FOLDER = "/home/"+username
SUB_FOLDER ="/Documents/Comptes"


# Execl used as tmp excel
class DataPath():
    def getDataPath(self):
        path_file = MAIN_FOLDER+SUB_FOLDER+"/code/data"

        return path_file

    def popEnd(self, name_directory):
        size = len(name_directory)
        for i in range(size-1,0,-1):
            if name_directory[i] == "/":
                break
        return name_directory[0:i]


# Excel Origin
class ExcelPath(DataPath):
    def __init__(self):
        self.excel_path = self.getProjectExcelPath()
        self._real_excel_path = self.getRealExcelPath()
    
    def getProjectExcelPath(self):
        path_data = self.getDataPath()
        name_file = "comptes.xlsx"
        project_excel = path_data + "/" + name_file
        return project_excel
        
    def getRealExcelPath(self):
        path_file = MAIN_FOLDER+SUB_FOLDER
        name_file = "expenses.xlsx"
        path_excel = path_file + "/" + name_file
        return path_excel



class DescrToThemePath(DataPath):        
    def getDescriptionToThemePath(self):
        path_conv = self.getDataPath() + "/convert_descr_to_theme.json"
        return path_conv
    


class ThemesAndSubthemesAuthorized(DataPath):        
    def getTSTPath(self):
        path_conv = self.getDataPath() + "/themes_subthemes_authorized.json"
        return path_conv
    

