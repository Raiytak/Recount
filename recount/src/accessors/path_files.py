# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This file contains the paths of the documents used in the app.
The manipulations of those files are done in other access_files or in the 
class directly.
"""

import os
import sys
import re
from pathlib import Path


# ROOT PATH of the project.
# Detected using the path from which the application is launched
def _getAppPath():
    root_path = os.path.abspath(__file__)
    app_path = Path(re.sub("(app).*", "app", root_path))
    return app_path


APP_PATH = _getAppPath()
if APP_PATH not in sys.path:
    sys.path = [APP_PATH] + sys.path
SRC_PATH = APP_PATH / "src"
DATA_PATH = APP_PATH / "data"
DATA_USERS_PATH = DATA_PATH / "users"


class PathInformation:
    root = ""
    folders = []
    filename = ""


class FilesPaths:
    """Paths to the folders used by the application"""

    def __init__(self, ROOT_PATH=SRC_PATH):
        self.PathInformation = PathInformation()
        self.PathInformation.root = ROOT_PATH
        self.data_folder = "data"
        self.excels_folder = "excels"
        self.example_folder = "examples"
        self.vues_folder = "vues"
        self.categories_folder = "categories"
        self.intelligent_fill = "intelligent_fill"
        self.standard_buttons = "standard_buttons"
        self.notebook_excel = "notebook_excel"
        self.config_folder = "config"
        self.users_data = "users"
        self.logs_folder = "logs"

    def joinPaths(self, root_path, filename, folders=None):
        if folders == None:
            return root_path / filename
        chained_folders = "/".join(folders)
        return root_path / chained_folders / filename

    def formPathUsing(self, pathInformation):
        root_path = pathInformation.root
        folders = pathInformation.folders
        filename = pathInformation.filename
        return self.joinPaths(root_path, filename, folders)

    def fileExists(self, folders=[], filename=""):
        self.PathInformation.folders = folders
        self.PathInformation.filename = filename
        path_file = self.formPathUsing(self.PathInformation)
        bool_exists = os.path.exists(path_file)
        return bool_exists, path_file


class ConfigPath(FilesPaths):
    """Path to the configs containing all the secrets of the application :
        -private keys that encrypt / decrypt the excels
        -users name and password
        -server certificates"""

    def __init__(self, ROOT_PATH=SRC_PATH):
        super().__init__(ROOT_PATH)

    def getApplicationConfigsPath(self):
        self.PathInformation.folders = [self.config_folder]
        self.PathInformation.filename = "app_configs.json"
        return self.formPathUsing(self.PathInformation)

    def getUsersPath(self):
        self.PathInformation.folders = [self.config_folder]
        self.PathInformation.filename = "users.json"
        return self.formPathUsing(self.PathInformation)

    def getKeysFolderPath(self):
        self.PathInformation.folders = [self.config_folder, "keys"]
        self.PathInformation.filename = ""
        return self.formPathUsing(self.PathInformation)

    def getCertificatePath(self):
        list_folders = [self.config_folder, "keys"]
        path_exists, path_created = self.fileExists(list_folders, "other-csr.pem")
        if path_exists:
            return path_created
        else:
            path_exists, path_created = self.fileExists(list_folders, "server-csr.pem")
            return self.formPathUsing(self.PathInformation)

    def getPrivateKeyPath(self):
        list_folders = [self.config_folder, "keys"]
        path_exists, path_created = self.fileExists(
            list_folders, "other-private-key.pem"
        )
        if path_exists:
            return path_created
        else:
            path_exists, path_created = self.fileExists(
                list_folders, "server-private-key.pem"
            )
            return path_created

    def getExcelKeyPath(self, name=""):
        self.PathInformation.folders = [self.config_folder, "keys"]
        if name == "":
            name = "excel.key"
        self.PathInformation.filename = name
        return self.formPathUsing(self.PathInformation)

    def getDataSqlKeyPath(self, name=""):
        self.PathInformation.folders = [self.config_folder, "keys"]
        if name == "":
            name = "data_sql.key"
        self.PathInformation.filename = name
        return self.formPathUsing(self.PathInformation)


class ExcelPaths(FilesPaths):
    """Path to the excels used :
        -source excel (from the user (saved / imported) or from the folder examples)
        -copy excel (copy of the source excel, cleaned and
                    manipulated by the application, then removed)"""

    def __init__(self, ROOT_PATH=DATA_PATH):
        super().__init__(ROOT_PATH)

    def importedExcelPath(self):
        self.PathInformation.folders = [self.excels_folder]
        self.PathInformation.filename = "imported_excel.xlsx"
        return self.formPathUsing(self.PathInformation)

    def cleanedExcelPath(self):
        self.PathInformation.folders = [self.excels_folder]
        self.PathInformation.filename = "cleaned_expenses.xlsx"
        return self.formPathUsing(self.PathInformation)

    def rawExcelPath(self):
        self.PathInformation.folders = [self.excels_folder]
        self.PathInformation.filename = "raw_expenses.xlsx"
        return self.formPathUsing(self.PathInformation)

    def exportExcelPath(self):
        if self.rawExcelExists():
            return self.rawExcelPath()
        return self.exampleExcelPath()

    def exampleExcelPath(self):
        TEMP_PATH = self.PathInformation.root

        self.PathInformation.root = DATA_PATH
        self.PathInformation.folders = [self.example_folder]
        self.PathInformation.filename = "example_expenses_en.xlsx"
        example_path = self.formPathUsing(self.PathInformation)

        self.PathInformation.root = TEMP_PATH
        return example_path

    def pathExists(self, my_path):
        is_present = os.path.exists(my_path)
        return is_present

    def importedExcelExists(self):
        return self.pathExists(self.importedExcelPath())

    def rawExcelExists(self):
        return self.pathExists(self.rawExcelPath())

    def copiedExcelExists(self):
        return self.pathExists(self.cleanedExcelPath())


class DescrToThemePath(FilesPaths):
    """Path to the file that converts description to a couple category theme (AI)"""

    def __init__(self, ROOT_PATH=DATA_PATH):
        super().__init__(ROOT_PATH)

    def getDescriptionToThemePath(self):
        self.PathInformation.folders = [self.categories_folder]
        self.PathInformation.filename = "convert_descr_to_theme.json"
        return self.formPathUsing(self.PathInformation)


class CategoryAndThemeAuthorizedPath(FilesPaths):
    """Path to the file that contains the authorized cat and theme by user"""

    # TODO: change this to for each user + save
    def __init__(self, ROOT_PATH=DATA_PATH):
        super().__init__(ROOT_PATH)

    def getCategoryAndThemePath(self):
        self.PathInformation.folders = [self.categories_folder]
        self.PathInformation.filename = "categories_themes_authorized.json"
        return self.formPathUsing(self.PathInformation)

    def getCategoryAndThemeTestPath(self):
        self.PathInformation.folders = [self.categories_folder]
        self.PathInformation.filename = "categories_themes_authorized_test.json"
        return self.formPathUsing(self.PathInformation)


class NotebookConfigPath(FilesPaths):
    """Path to the file that contains the saved information of the notebook of each user"""

    # TODO: change this to for each user + save
    def __init__(self, ROOT_PATH=DATA_PATH):
        super().__init__(ROOT_PATH)

    def getNotebookConfigPath(self):
        self.PathInformation.folders = [self.notebook_excel]
        self.PathInformation.filename = "categories_themes_authorized_test.json"
        return self.formPathUsing(self.PathInformation)


class StandardButtonsConfigPath(FilesPaths):
    """Path to the file that contains the saved information of the buttons of each user"""

    # TODO: change this to for each user + save
    def __init__(self, ROOT_PATH=DATA_PATH):
        super().__init__(ROOT_PATH)

    def getStandardButtonsConfigPath(self):
        self.PathInformation.folders = [self.vues_folder, self.standard_buttons]
        self.PathInformation.filename = "config_buttons.json"
        return self.formPathUsing(self.PathInformation)


class UserDataPath(FilesPaths):
    """Path to the files of the designated user"""

    def __init__(self, username):
        USER_DATA_PATH = DATA_USERS_PATH / username
        super().__init__(USER_DATA_PATH)

    def userFolderExists(self, name_folder=""):
        return self.fileExists(folders=[name_folder])

    def userMainFolderExists(self):
        return self.userFolderExists()

    def userExcelsFolderExists(self):
        return self.userFolderExists(self.excels_folder)

    def userNotebookFolderExists(self):
        return self.userFolderExists(self.notebook_excel)
