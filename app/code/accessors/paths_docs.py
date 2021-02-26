# -*- coding: utf-8 -*-

# === DESCRIPTION ===
# This file aims to do return the paths of the documents used in the app.
# The manipulations are done in other modules.

from shutil import copyfile
import json

import pandas as pd

import os


# Path to the file data used by the application
class ApplicationDataPath():
    def __init__(self, config_json):
        self.config_json = config_json

        self.folder_to_excels = "excels"
        self.folder_to_vues = "vues"
        self.folder_to_categories = "categories"


    def getDataPath(self):
        path_data = self.config_json["paths"]["PATH_TO_MAIN_FOLDER"] + "/code/data"
        return path_data

    def getMainPath(self):
        path_main_folder = self.config_json["paths"]["PATH_TO_MAIN_FOLDER"]
        return path_main_folder

    # TODO
    # def getExcelPath(self):
    #     path_data = self.config_json["paths"]["PATH_TO_MAIN_FOLDER"] + "/code/data"
    #     return path_data


# Path to the excels used : 
#   the source excel (from the user or excel_example) 
#   and the copy excel (copied, cleaned and manipulated by the applciation)
class ExcelPath(ApplicationDataPath):
    def __init__(self, config_json):
        super().__init__(config_json)

        self._excel_path = self.copiedExcelPath()
        self._source_excel_path = self.importedExcelPath()


    def nameImportedExcel(self):
        return "imported_excel.xlsx"

    def nameImportedExcelOfTypeCSVTemporary(self):
        return "imported_temporary_excel.csv"

        
        
    def importedExcelPath(self):
        path_file = self.getDataPath()
        name_folder_excels = self.folder_to_excels
        name_file = self.nameImportedExcel()
        path_excel = path_file + "/" + name_folder_excels + "/" + name_file
        return path_excel
    def importedTemporaryCSVExcelPath(self):
        path_file = self.getDataPath()
        name_folder_excels = self.folder_to_excels
        name_file = self.nameImportedExcelOfTypeCSVTemporary()
        path_excel = path_file + "/" + name_folder_excels + "/" + name_file
        return path_excel
    
    def copiedExcelPath(self):
        path_file = self.getDataPath()
        name_folder_excels = self.folder_to_excels
        name_file = "copy_expenses.xlsx"
        project_excel = path_file + "/" + name_folder_excels + "/" + name_file
        return project_excel
    
    def rawCopiedExcelPath(self):
        path_file = self.getDataPath()
        name_folder_excels = self.folder_to_excels
        name_file = "raw_copy_expenses.xlsx"
        raw_copy_excel = path_file + "/" + name_folder_excels + "/" + name_file
        return raw_copy_excel

    def exampleExcelPath(self):
        path_file = self.getMainPath()
        name_file = "documentation/example_expenses_en.xlsx"
        path_excel = path_file + "/" + name_file
        return path_excel


    def pathExists(self, my_path):
        is_present = os.path.exists(my_path)
        return is_present
    def rawCopiedExcelExists(self):
        return self.pathExists(self.rawCopiedExcelPath())
    def copiedExcelExists(self):
        return self.pathExists(self.copiedExcelPath())



class DescrToThemePath(ApplicationDataPath):       
    def __init__(self, config_json):
        super().__init__(config_json)
        self.folder_to_intell_fill = "intelligent_fill"

    def getDescriptionToThemePath(self):
        name_folder_excels = self.folder_to_categories
        path_conv = self.getDataPath() + "/" + name_folder_excels + "/" + self.folder_to_intell_fill + "/convert_descr_to_theme.json"
        return path_conv
    


class CategoryAndThemeAuthorizedPath(ApplicationDataPath):     
    def __init__(self, config_json):
        super().__init__(config_json)

    def getCategoryAndThemePath(self):
        name_folder_categories = self.folder_to_categories
        # path_conv = self.getDataPath() + "/themes_subthemes_authorized.json"
        path_conv = self.getDataPath() + "/" + name_folder_categories + "/categories_themes_authorized.json"
        return path_conv

    def getCategoryAndThemeTestPath(self):
        name_folder_categories = self.folder_to_categories
        # path_conv = self.getDataPath() + "/themes_subthemes_authorized.json"
        path_conv = self.getDataPath() + "/" + name_folder_categories + "/categories_themes_authorized_test.json"
        return path_conv
    
    


class NotebookConfigPath(ApplicationDataPath):        
    def __init__(self, config_json):
        super().__init__(config_json)

    def getNotebookConfigPath(self):
        name_folder_vues = self.folder_to_vues
        # path_conv = self.getDataPath() + "/themes_subthemes_authorized.json"
        path_conf = self.getDataPath() + "/" + name_folder_vues + "/notebook_excel/config_notebook.json"
        return path_conf
    

class StandardButtonsConfigPath(ApplicationDataPath):        
    def __init__(self, config_json):
        super().__init__(config_json)
        self.folder_to_buttons = "standard_buttons"

    def getStandardButtonsConfigPath(self):
        name_folder_vues = self.folder_to_vues
        # path_conv = self.getDataPath() + "/themes_subthemes_authorized.json"
        path_conf = self.getDataPath() + "/" + name_folder_vues + "/" + self.folder_to_buttons + "/config_buttons.json"
        return path_conf
    




