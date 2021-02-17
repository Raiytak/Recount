# -*- coding: utf-8 -*-
from shutil import copyfile
import json

import pandas as pd

import getpass


username = getpass.getuser()
USER_HOME = "/home/"+username
PATH_TO_MAIN_FOLDER ="/Desktop/Projets/Comptes"


# Path to the file data used by the application
class ApplicationDataPath():
    def getDataPath(self):
        path_file = USER_HOME+PATH_TO_MAIN_FOLDER+"/code/data"
        return path_file

    def popEnd(self, name_directory):
        size = len(name_directory)
        for i in range(size-1,0,-1):
            if name_directory[i] == "/":
                break
        return name_directory[0:i]


# Path to the excels used : 
#   the source excel (from user) 
#   and the copy excel (copied and cleaned by the applciation)
class ExcelPath(ApplicationDataPath):
    def __init__(self):
        self.excel_path = self.getCopiedExcelPath()
        self._source_excel_path = self.getSourceExcelPath()
        
    def getSourceExcelPath(self):
        path_file = USER_HOME+PATH_TO_MAIN_FOLDER
        name_file = "expenses.xlsx"
        path_excel = path_file + "/" + name_file
        return path_excel
    
    def getCopiedExcelPath(self):
        path_file = self.getDataPath()
        name_file = "comptes.xlsx"
        project_excel = path_file + "/" + name_file
        return project_excel



class DescrToThemePath(ApplicationDataPath):        
    def getDescriptionToThemePath(self):
        path_conv = self.getDataPath() + "/convert_descr_to_theme.json"
        return path_conv
    


class ThemesAndSubthemesAuthorized(ApplicationDataPath):        
    def getTSTPath(self):
        path_conv = self.getDataPath() + "/themes_subthemes_authorized.json"
        return path_conv
    

