# -*- coding: utf-8 -*-

# === DESCRIPTION ===
# This file aims to do return the paths of the documents used in the app.
# The manipulations are done in other modules.

import os


# Path to the file data used by the application
class ApplicationDataPath:
    def __init__(self):
        self.folder_to_excels = "excels"
        self.folder_to_examples = "examples"
        self.folder_to_vues = "vues"
        self.folder_to_categories = "categories"

    def getDataPath(self):
        path_data = "data"
        return path_data


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

    def joinPaths(self, root_path, file, folder=None):
        if folder==None:
            return root_path + "/" + file
        return root_path + "/" + folder + "/" + file

    def importedExcelPath(self):
        path_file = self.getDataPath()
        folder_excels = self.folder_to_excels
        name_file = self.nameImportedExcel()
        return self.joinPaths(path_file, name_file, folder_excels)

    def importedTemporaryCSVExcelPath(self):
        path_file = self.getDataPath()
        folder_excels = self.folder_to_excels
        name_file = self.nameImportedExcelOfTypeCSVTemporary()
        return self.joinPaths(path_file, name_file, folder_excels)

    def copiedExcelPath(self):
        path_file = self.getDataPath()
        folder_excels = self.folder_to_excels
        name_file = "copy_expenses.xlsx"
        return self.joinPaths(path_file, name_file, folder_excels)

    def rawCopiedExcelPath(self):
        path_file = self.getDataPath()
        folder_excels = self.folder_to_excels
        name_file = "raw_copy_expenses.xlsx"
        return self.joinPaths(path_file, name_file, folder_excels)

    def exampleExcelPath(self):
        path_file = self.getDataPath()
        folder_excels = self.folder_to_examples
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
        self.folder_to_intell_fill = "intelligent_fill"

    def getDescriptionToThemePath(self):
        name_folder_excels = self.folder_to_categories
        path_conv = (
            self.getDataPath()
            + "/"
            + name_folder_excels
            + "/"
            + self.folder_to_intell_fill
            + "/convert_descr_to_theme.json"
        )
        return path_conv


class CategoryAndThemeAuthorizedPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getCategoryAndThemePath(self):
        name_folder_categories = self.folder_to_categories
        path_conv = (
            self.getDataPath()
            + "/"
            + name_folder_categories
            + "/categories_themes_authorized.json"
        )
        return path_conv

    def getCategoryAndThemeTestPath(self):
        name_folder_categories = self.folder_to_categories
        path_conv = (
            self.getDataPath()
            + "/"
            + name_folder_categories
            + "/categories_themes_authorized_test.json"
        )
        return path_conv


class NotebookConfigPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getNotebookConfigPath(self):
        name_folder_vues = self.folder_to_vues
        path_conf = (
            self.getDataPath()
            + "/"
            + name_folder_vues
            + "/notebook_excel/config_notebook.json"
        )
        return path_conf


class StandardButtonsConfigPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()
        self.folder_to_buttons = "standard_buttons"

    def getStandardButtonsConfigPath(self):
        name_folder_vues = self.folder_to_vues
        path_conf = (
            self.getDataPath()
            + "/"
            + name_folder_vues
            + "/"
            + self.folder_to_buttons
            + "/config_buttons.json"
        )
        return path_conf
