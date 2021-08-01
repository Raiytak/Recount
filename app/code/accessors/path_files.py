# -*- coding: utf-8 -*-

# === DESCRIPTION ===
# This file aims to do return the paths of the documents used in the app.
# The manipulations are done in other modules.

import os
import sys
import re


def _getCodePath():
    root_path = os.path.abspath(__file__)
    app_path = re.sub("(app).*", "app", root_path)
    code_path = os.path.join(app_path, "code")
    return code_path


CODE_PATH = _getCodePath()
if CODE_PATH not in sys.path:
    sys.path = [CODE_PATH] + sys.path


class PathInformation:
    root = CODE_PATH
    folders = []
    filename = ""


# Path to the file data used by the application
class ApplicationDataPath:
    def __init__(self):
        self.PathInformation = PathInformation
        self.folder_data = "data"
        self.excels_folder = "excels"
        self.example_folder = "examples"
        self.vues_folder = "vues"
        self.categories_folder = "categories"
        self.intelligent_fill = "intelligent_fill"
        self.standard_buttons = "standard_buttons"
        self.notebook_excel = "notebook_excel"
        self.folder_config = "config"

    def joinPaths(self, root_path, filename, folders=None):
        if folders == None:
            return root_path + "/" + filename
        chained_folders = "/".join(folders)
        return root_path + "/" + chained_folders + "/" + filename

    def formPathUsing(self, pathInformation):
        root_path = pathInformation.root
        folders = pathInformation.folders
        filename = pathInformation.filename
        return self.joinPaths(root_path, filename, folders)


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
        self.PathInformation.folders = [self.folder_data, self.excels_folder]
        self.PathInformation.filename = self.nameImportedExcel()
        return self.formPathUsing(self.PathInformation)

    def importedTemporaryCSVExcelPath(self):
        self.PathInformation.folders = [self.folder_data, self.excels_folder]
        self.PathInformation.filename = self.nameImportedExcelOfTypeCSVTemporary()
        return self.formPathUsing(self.PathInformation)

    def copiedExcelPath(self):
        self.PathInformation.folders = [self.folder_data, self.excels_folder]
        self.PathInformation.filename = "copy_expenses.xlsx"
        return self.formPathUsing(self.PathInformation)

    def rawCopiedExcelPath(self):
        self.PathInformation.folders = [self.folder_data, self.excels_folder]
        self.PathInformation.filename = "raw_copy_expenses.xlsx"
        return self.formPathUsing(self.PathInformation)

    def exampleExcelPath(self):
        self.PathInformation.folders = [self.folder_data, self.example_folder]
        self.PathInformation.filename = "example_expenses_en.xlsx"
        return self.formPathUsing(self.PathInformation)

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
        self.PathInformation.folders = [self.folder_data, self.categories_folder]
        self.PathInformation.filename = "convert_descr_to_theme.json"
        return self.formPathUsing(self.PathInformation)


class CategoryAndThemeAuthorizedPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getCategoryAndThemePath(self):
        self.PathInformation.folders = [self.folder_data, self.categories_folder]
        self.PathInformation.filename = "categories_themes_authorized.json"
        return self.formPathUsing(self.PathInformation)

    def getCategoryAndThemeTestPath(self):
        self.PathInformation.folders = [self.folder_data, self.categories_folder]
        self.PathInformation.filename = "categories_themes_authorized_test.json"
        return self.formPathUsing(self.PathInformation)


class NotebookConfigPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getNotebookConfigPath(self):
        self.PathInformation.folders = [self.folder_data, self.notebook_excel]
        self.PathInformation.filename = "categories_themes_authorized_test.json"
        return self.formPathUsing(self.PathInformation)


class StandardButtonsConfigPath(ApplicationDataPath):
    def __init__(self):
        super().__init__()

    def getStandardButtonsConfigPath(self):
        self.PathInformation.folders = [
            self.folder_data,
            self.vues_folder,
            self.standard_buttons,
        ]
        self.PathInformation.filename = "config_buttons.json"
        return self.formPathUsing(self.PathInformation)
