# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This file aims to do the CRUD manipulations on the USER files used by the application.
The paths used are stored in the paths_docs module, and are used by the wrappers of this module.
"""

"""ATTENTION: To access user files, you should always do it using AccessUserFiles class !"""


from shutil import copyfile

import pandas as pd
import json
import os
import logging

from accessors.path_files import *
from accessors.data_encryption import ExcelEncryption


class AccessExcel:
    """CRUD operations on all the excels of the application"""

    def __init__(self, ROOT_PATH=DATA_PATH):
        self.ExcelPaths = ExcelPaths(ROOT_PATH)
        # self.useExampleIfNoRawExcel()

    def getExcelFile(self, path_excel):
        with open(path_excel, "rb") as file:
            excel_file = file.read()
        return excel_file

    def copyImportedExcelIfExists(self):
        if self.ExcelPaths.importedExcelExists() == True:
            self.copyImportedExcel()

    def useExampleIfNoRawExcel(self):
        if self.ExcelPaths.rawExcelExists() == False:
            self.copyExampleExcel()

    def copyRawExcel(self):
        copyfile(self.ExcelPaths.rawExcelPath(), self.ExcelPaths.cleanedExcelPath())

    def copyImportedExcel(self):
        copyfile(self.ExcelPaths.importedExcelPath(), self.ExcelPaths.rawExcelPath())

    def copyExampleExcel(self):
        copyfile(self.ExcelPaths.exampleExcelPath(), self.ExcelPaths.rawExcelPath())

    def removeFile(self, path_file):
        try:
            os.remove(path_file)
        except FileNotFoundError:
            pass

    def removeImportedExcel(self):
        self.removeFile(self.ExcelPaths.importedExcelPath())

    def removeCleanedExcel(self):
        self.removeFile(self.ExcelPaths.cleanedExcelPath())

    def removeRawExcel(self):
        self.removeFile(self.ExcelPaths.rawExcelPath())

    def removeAllExcels(self):
        self.removeRawExcel()
        self.removeCleanedExcel()
        self.removeImportedExcel()

    def removeAllExcelsExceptRaw(self):
        self.removeCleanedExcel()
        self.removeImportedExcel()

    def removeAllOldFiles(self):
        if self.ExcelPaths.rawExcelExists() == True:
            self.removeRawExcel()
        if self.ExcelPaths.cleanedExcelPath() == True:
            self.removeCleanedExcel()

    def updateUserExcel(self):
        if self.ExcelPaths.importedExcelExists() == True:
            self.copyImportedExcel()
        if self.ExcelPaths.rawExcelExists() == True:
            self.copyRawExcel()
        else:
            raise FileNotFoundError("No Raw excel neither imported excel")


class AccessDescrToTheme:
    """CRUD operations on the descr_to_theme files of the application"""

    # TODO: change this to for each user + save
    def __init__(self):
        self.DescrToThemePath = DescrToThemePath()

    def getJsonDescrToTheme(self):
        data = {}
        try:
            with open(
                self.DescrToThemePath.getDescriptionToThemePath(), "r"
            ) as json_file:
                data = json.load(json_file)
        # Case where the document isn't created yet
        except FileNotFoundError:
            self.updateDescrConvJson(data)

        return data

    def updateDescrConvJson(self, data):
        with open(self.DescrToThemePath.getDescriptionToThemePath(), "w") as json_file:
            try:
                json.dump(data, json_file)
            except TypeError:
                logging.exception("JSON of wrong type :\n", data)


class AccessCTAuthorized:
    """CRUD operations on the cat_theme_auth files of the application"""

    # TODO: change this to for each user + save
    def __init__(self):
        self.TSTAuth = CategoryAndThemeAuthorizedPath()

    def getJson(self):
        data = {}
        with open(self.TSTAuth.getCategoryAndThemePath(), "r") as json_file:
            data = json.load(json_file)
        return data

    def updateJson(self, data):
        with open(self.TSTAuth.getCategoryAndThemePath(), "w") as json_file:
            try:
                json.dump(data, json_file, indent=4)
            except TypeError:
                logging.exception("JSON of wrong type :\n", data)

    def getPrettyJson(self):
        data = self.getJson()
        json_formatted_str = json.dumps(data, indent=4)
        return json_formatted_str

    def getTestJson(self):
        data = {}
        with open(self.TSTAuth.getCategoryAndThemeTestPath(), "r") as json_file:
            data = json.load(json_file)
        return data


class AccessNotebookConfig:
    """CRUD operations on the notebook confs of the application"""

    # TODO: change this to for each user + save
    def __init__(self):
        self.NotebookConfigPath = NotebookConfigPath()

    def getJson(self):
        data = {}
        with open(self.NotebookConfigPath.getNotebookConfigPath(), "r") as json_file:
            data = json.load(json_file)
        return data

    def updateJson(self, data):
        with open(self.NotebookConfigPath.getNotebookConfigPath(), "w") as json_file:
            try:
                json.dump(data, json_file, indent=4)
            except TypeError:
                logging.exception("JSON of wrong type :\n", data)

    def getPrettyJson(self):
        data = self.getJson()
        json_formatted_str = json.dumps(data, indent=4)
        return json_formatted_str


class AccessStandardButtonsConfig:
    """CRUD operations on the button confs of the application"""

    # TODO: change this to for each user + save
    def __init__(self):
        self.StandardButtonsConfigPath = StandardButtonsConfigPath()

    def getJson(self):
        data = {}
        with open(
            self.StandardButtonsConfigPath.getStandardButtonsConfigPath(), "r"
        ) as json_file:
            data = json.load(json_file)
        return data

    def updateJson(self, data):
        with open(
            self.StandardButtonsConfigPath.getStandardButtonsConfigPath(), "w"
        ) as json_file:
            try:
                json.dump(data, json_file, indent=4)
            except TypeError:
                logging.exception("JSON of wrong type :\n", data)

    def getPrettyJson(self):
        data = self.getJson()
        json_formatted_str = json.dumps(data, indent=4)
        return json_formatted_str


class AccessUserFiles:
    """CRUD operations on the files of the users"""

    def __init__(self, username):
        self.UserDataPath = UserDataPath(username)
        ROOT_PATH = DATA_USERS_PATH / username
        self.AccessExcel = AccessExcel(ROOT_PATH)
        self.ExcelEncryption = ExcelEncryption()

        self.createUserFolders()
        # self.removeOlderFiles()
        self.initializeUserFolders()

    def createUserFolders(self):
        self.createUserMainFolder()
        self.createUserExcelsFolder()
        self.createUserNotebookFolder()

    def createUserMainFolder(self):
        self.createFolder(self.UserDataPath.userMainFolderExists)

    def createUserExcelsFolder(self):
        self.createFolder(self.UserDataPath.userExcelsFolderExists)

    def createUserNotebookFolder(self):
        self.createFolder(self.UserDataPath.userNotebookFolderExists)

    def createFolder(self, folderExists):
        is_created, folder_path = folderExists()
        if is_created == False:
            try:
                os.mkdir(folder_path)
            except Exception as e:
                logging.exception(
                    f"Exception occured during the creation of the user's main folder  : {e}"
                )

    # TODO
    def removeOlderFiles(self):
        are_created, user_path = self.AccessExcel.ExcelPaths.fileUserExists()
        if are_created == False:
            try:
                os.mkdir(user_path)
            except Exception as e:
                logging.exception(f"Exception occured during user file creation : {e}")

    def initializeUserFolders(self):
        self.AccessExcel.copyImportedExcelIfExists()
        self.AccessExcel.useExampleIfNoRawExcel()
        # self.AccessExcel.updateUserExcel()

    def removeExcelsOfUser(self):
        self.AccessExcel.removeAllExcels()

    def removeExcelsExceptRawOfUser(self):
        self.AccessExcel.removeAllExcelsExceptRaw()
