# -*- coding: utf-8 -*-

# === DESCRIPTION ===
# This file aims to do return the paths of the documents used in the app.
# The manipulations are done in other modules.

import os


# Path to the file data used by the application
class ApplicationDataPath:
    def __init__(self):
        self.CODE_PATH = os.environ["CODE_PATH"]
        self.folder_data = "data"
        self.excels_folder = "excels"
        self.example_folder = "examples"
        self.vues_folder = "vues"
        self.categories_folder = "categories"
        self.intelligent_fill = "intelligent_fill"
        self.standard_buttons = "standard_buttons"
        self.notebook_excel = "notebook_excel"
        

    def joinPaths(self, root_path, file, folders=None):
        if folders==None:
            return root_path + "/" + file
        chained_folders = "/".join(folders)
        return root_path + "/" + chained_folders + "/" + file


# Path to the excels used :
#   the source excel (from the user or excel_example)
#   and the copy excel (copied, cleaned and manipulated by the applciation)
class ExcelPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()
        self._excel_path = self.copiedExcelPath()
        self._source_excel_path = self.importedExcelPath()

    def nameImportedExcel(self):
        return "imported_excel.xlsx"

    def nameImportedExcelOfTypeCSVTemporary(self):
        return "imported_temporary_excel.csv"

    def importedExcelPath(self):
        path_file = self.CODE_PATH
        folder_excels = [self.folder_data, self.excels_folder]
        name_file = self.nameImportedExcel()
        return self.joinPaths(path_file, name_file, folder_excels)

    def importedTemporaryCSVExcelPath(self):
        path_file = self.CODE_PATH
        folder_excels = [self.folder_data, self.excels_folder]
        name_file = self.nameImportedExcelOfTypeCSVTemporary()
        return self.joinPaths(path_file, name_file, folder_excels)

    def copiedExcelPath(self):
        path_file = self.CODE_PATH
        folder_excels = [self.folder_data, self.excels_folder]
        name_file = "copy_expenses.xlsx"
        return self.joinPaths(path_file, name_file, folder_excels)

    def rawCopiedExcelPath(self):
        path_file = self.CODE_PATH
        folder_excels = [self.folder_data, self.excels_folder]
        name_file = "raw_copy_expenses.xlsx"
        return self.joinPaths(path_file, name_file, folder_excels)

    def exampleExcelPath(self):
        path_file = self.CODE_PATH
        folder_excels = [self.folder_data, self.example_folder]
        name_file = "example_expenses_en.xlsx"
        return self.joinPaths(path_file, name_file, folder_excels)

    def pathExists(self, my_path):
        is_present = os.path.exists(my_path)
        return is_present

    def rawCopiedExcelExists(self):
        return self.pathExists(self.rawCopiedExcelPath())

    def copiedExcelExists(self):
        return self.pathExists(self.copiedExcelPath())


class DescrToThemePath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getDescriptionToThemePath(self):
        path_file = self.CODE_PATH
        folders = [self.folder_data, self.categories_folder]
        name_file = "convert_descr_to_theme.json"
        return self.joinPaths(path_file, name_file, folders)


class CategoryAndThemeAuthorizedPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getCategoryAndThemePath(self):
        path_file = self.CODE_PATH
        folders = [self.folder_data, self.categories_folder]
        name_file = "categories_themes_authorized.json"
        return self.joinPaths(path_file, name_file, folders)

    def getCategoryAndThemeTestPath(self):
        path_file = self.CODE_PATH
        folders = [self.folder_data, self.categories_folder]
        name_file = "categories_themes_authorized_test.json"
        return self.joinPaths(path_file, name_file, folders)


class NotebookConfigPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getNotebookConfigPath(self):
        path_file = self.CODE_PATH
        folders = [self.folder_data, self.notebook_excel]
        name_file = "categories_themes_authorized_test.json"
        return self.joinPaths(path_file, name_file, folders)


class StandardButtonsConfigPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getStandardButtonsConfigPath(self):
        path_file = self.CODE_PATH
        folders = [self.folder_data, self.vues_folder, self.standard_buttons]
        name_file = "config_buttons.json"
        return self.joinPaths(path_file, name_file, folders)
