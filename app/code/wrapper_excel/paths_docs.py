# -*- coding: utf-8 -*-
from shutil import copyfile
import json

import pandas as pd

import os


# Path to the file data used by the application
class ApplicationDataPath():
    def __init__(self, config_json):
        self.config_json = config_json

    def getDataPath(self):
        path_data = self.config_json["paths"]["PATH_TO_MAIN_FOLDER"] + "/code/data"
        return path_data

    def getMainPath(self):
        path_main_folder = self.config_json["paths"]["PATH_TO_MAIN_FOLDER"]
        return path_main_folder

    def popEnd(self, name_directory):
        size = len(name_directory)
        for i in range(size-1,0,-1):
            if name_directory[i] == "/":
                break
        return name_directory[0:i]


# Path to the excels used : 
#   the source excel : 
#       imported = imported by the user
#       example = means no file has been imported yet
#   and the copy excel (copied, cleaned and manipulated by the applciation)
class ExcelPath(ApplicationDataPath):
    def __init__(self, config_json):
        ApplicationDataPath.__init__(self, config_json)
        self._excel_path = self.copiedExcelPath()
        self._source_excel_path = self.importedExcelPath()
        self.config_json = config_json
        
    def importedExcelPath(self):
        path_file = self.getDataPath()
        name_file = "imported_expenses.xlsx"
        path_excel = path_file + "/" + name_file
        return path_excel
    
    def copiedExcelPath(self):
        path_file = self.getDataPath()
        name_file = "copy_expenses.xlsx"
        project_excel = path_file + "/" + name_file
        return project_excel

    def exampleExcelPath(self):
        path_file = self.getMainPath()
        name_file = "/documentation/example_expenses.xlsx"
        path_excel = path_file + "/" + name_file
        return path_excel


    def importedExcelExists(self):
        is_present = os.path.exists(self.importedExcelPath())
        return is_present



class DescrToThemePath(ApplicationDataPath):        
    def getDescriptionToThemePath(self):
        path_conv = self.getDataPath() + "/convert_descr_to_theme.json"
        return path_conv
    


class ThemesAndSubthemesAuthorized(ApplicationDataPath):        
    def getTSTPath(self):
        path_conv = self.getDataPath() + "/themes_subthemes_authorized.json"
        return path_conv
    

