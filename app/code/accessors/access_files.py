# -*- coding: utf-8 -*-

# === DESCRIPTION ===
# This file aims to do the CRUD manipulations on the files used by the application.
# The paths used are stored in the paths_docs module, and are used by the wrappers of this module.

from shutil import copyfile

import pandas as pd
import json
import os

from accessors.path_files import *


class AccessExcel:
    def __init__(self):
        self.ExcelPath = ExcelPath()
        self.useExampleIfNoExcel()

        # self.removeAllOldFiles()

    def useExampleIfNoExcel(self):
        if self.ExcelPath.rawCopiedExcelExists():
            self.copyRawExcel()
        else:
            self.copyExampleExcel()

    def copyRawExcel(self):
        copyfile(self.ExcelPath.rawCopiedExcelPath(), self.ExcelPath.copiedExcelPath())

    def copyExampleExcel(self):
        copyfile(self.ExcelPath.exampleExcelPath(), self.ExcelPath.copiedExcelPath())
        copyfile(self.ExcelPath.exampleExcelPath(), self.ExcelPath.rawCopiedExcelPath())

    def removeFile(self, path_file):
        try:
            os.remove(path_file)
        except FileNotFoundError:
            pass

    def removeCopiedExcel(self):
        self.removeFile(self.ExcelPath.copiedExcelPath())

    def removeRawCopiedExcel(self):
        self.removeFile(self.ExcelPath.rawCopiedExcelPath())

    def removeAllOldFiles(self):
        if self.ExcelPath.rawCopiedExcelExists() == True:
            self.removeRawCopiedExcel()
        if self.ExcelPath.copiedExcelPath() == True:
            self.removeCopiedExcel()

    def _updateExcel(self):
        if self.ExcelPath.rawCopiedExcelExists() == True:
            self.copyRawExcel()


class AccessDescrToTheme:
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
                print("JSON of wrong type :\n", data)


class AccessCTAuthorized:
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
                print("JSON of wrong type :\n", data)

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
                print("JSON of wrong type :\n", data)

    def getPrettyJson(self):
        data = self.getJson()
        json_formatted_str = json.dumps(data, indent=4)
        return json_formatted_str


class AccessStandardButtonsConfig:
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
                print("JSON of wrong type :\n", data)

    def getPrettyJson(self):
        data = self.getJson()
        json_formatted_str = json.dumps(data, indent=4)
        return json_formatted_str
