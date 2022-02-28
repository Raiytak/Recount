# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This file aims to do the CRUD manipulations on the files used by the application.
The paths used are stored in the paths_docs module, and are used by the wrappers of this module.
"""

"""ACHTUNG: To access user files, you should always do it using UserFilesAccess class !"""


import shutil
import json
import os
import io
from typing import Union
import pandas
import urllib.request
from currency_converter import ECB_URL

from .path_files import *

from cryptography.fernet import Fernet

__all__ = ["ConfigAccess", "LogAccess", "UserFilesAccess"]


def isExcel(file_path):
    # TODO 2496: use openpyxl instead
    excel_sigs = [
        (b"\x50\x4B\x05\x06", 2, -22, 4),
        (b"\x09\x08\x10\x00\x00\x06\x05\x00", 0, 512, 8),  # Saved from Excel
        (
            b"\x09\x08\x10\x00\x00\x06\x05\x00",
            0,
            1536,
            8,
        ),  # Saved from LibreOffice Calc
        (
            b"\x09\x08\x10\x00\x00\x06\x05\x00",
            0,
            2048,
            8,
        ),  # Saved from Excel then saved from Calc
    ]

    for sig, whence, offset, size in excel_sigs:
        with open(file_path, "rb") as file:
            file.seek(offset, whence)  # Seek to the offset.
            bytes = file.read(size)  # Capture the specified number of bytes.
            if bytes == sig:
                return True
    return False


def isExchangeRatesFileUpToDate():
    if len(ConfigPath.currencies_rates_filenames) == 0:
        return False
    return (
        ConfigPath.currencies_rates.name == ConfigPath.today_currencies_rates_filename
    )


def updateCurrenciesRates():
    # Delete the older file
    for filename in ConfigPath.currencies_rates_filenames:
        ConfigAccess.removeFile(ConfigPath.formPathUsing(ConfigPath.root, filename))
    # Import the currencies rates up to date
    urllib.request.urlretrieve(ECB_URL, ConfigPath.currencies_rates)


class FileAccessor:
    @staticmethod
    def dataOf(file_path):
        with open(file_path, "r") as file:
            data = file.read()
        return data

    @staticmethod
    def write(file_path, data: str):
        with open(file_path, "w") as file:
            file.write(data)

    @staticmethod
    def dataOfBinary(file_path: Path):
        with open(file_path, "rb") as file:
            data = file.read()
        return data

    @staticmethod
    def writeBinary(file_path: Path, data):
        with open(file_path, "wb") as file:
            file.write(data)

    @staticmethod
    def dataOfJson(file_path: Path):
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def writeJson(file_path: Path, data: dict):
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def removeFile(file_path):
        if FilePath.pathExists(file_path):
            os.remove(file_path)


class ConfigAccess(FileAccessor):
    """CRUD operations on the config files of the application"""

    class AppStages(Enum):
        DEVELOPMENT = "development"
        PRODUCTION = "production"

    @classproperty
    def database_config(cls):
        stage = os.getenv("RECOUNT_STAGE")
        app_configs = cls.app_configs
        db_configs = app_configs[stage]["mysql"]
        return db_configs

    @classproperty
    def app_configs(cls):
        with open(ConfigPath.application, "r") as json_file:
            data = json.load(json_file)
        return data

    @classproperty
    def currencies(cls):
        return cls.dataOfJson(ConfigPath.currencies)

    @classproperty
    def currencies_rates_path(cls):
        if not isExchangeRatesFileUpToDate():
            updateCurrenciesRates()
        return ConfigPath.currencies_rates

    @classproperty
    def excel_key(cls):
        return cls.dataOfBinary(ConfigPath.excel_key)

    @classproperty
    def sql_ey(cls):
        return cls.dataOfBinary(ConfigPath.sql_ey)

    @classproperty
    def users(cls):
        return cls.dataOfJson(ConfigPath.users)

    # TODO 5155: add SSL context
    @classproperty
    def ssl_context(cls):
        cert_file = ConfigPath.certificate
        private_key_file = ConfigPath.privateKey
        return (cert_file, private_key_file)


class LogAccess(FileAccessor):
    """CRUD operations on the log files of the application"""

    @classmethod
    def removeLogs(cls):
        for log_path in LogPath.logs_path:
            cls.removeFile(log_path)


class UserFilesAccess(FileAccessor):
    """CRUD operations on all the excels of the application"""

    def __init__(self, username: str = None):
        self.fernet_encryption = FernetEncryption(ConfigAccess.excel_key)
        if username is None:
            self.user_files_path = UserFilesPath
        else:
            self.user_files_path = UserFilesPath(username)
            self.initializeUserFolders()

    def initializeUserFolders(self):
        if not FilePath.pathExists(self.user_files_path.user_folder):
            self.createUserFolder()
        if not FilePath.pathExists(self.user_files_path.excel):
            self.copyAndEncryptExampleExcel()
        if not FilePath.pathExists(self.user_files_path.categories):
            shutil.copy(
                UserFilesPath.example_categories, self.user_files_path.categories
            )
        if not FilePath.pathExists(self.user_files_path.intelligent_fill):
            shutil.copy(
                UserFilesPath.example_intelligent_fill,
                self.user_files_path.intelligent_fill,
            )
        if not FilePath.pathExists(self.user_files_path.translations):
            shutil.copy(
                UserFilesPath.example_translations, self.user_files_path.translations,
            )

    def createUserFolder(self):
        os.mkdir(self.user_files_path.user_folder)

    def removeUserFolder(self):
        if FilePath.pathExists(self.user_files_path.user_folder):
            shutil.rmtree(self.user_files_path.user_folder, ignore_errors=False)

    def excel(self, excel_path: Path = None):
        """If no path is provided, gets the 'expenses.xlsx' of the selected
        user, or the example one if no user is given"""
        if excel_path is None:
            if self.user_files_path.pathExists(self.user_files_path.excel):
                excel_path = self.user_files_path.excel
            else:
                excel_path = self.user_files_path.example_excel
        is_excel = self.isDecryptedExcelFile(excel_path)
        if is_excel == True:
            data = self.dataOfBinary(excel_path)
        elif is_excel == False:
            encrypted_data = self.dataOfBinary(excel_path)
            data = self.fernet_encryption.decryptData(encrypted_data)
        return data

    def dataframe(self, excel_path: Path = None):
        return pandas.read_excel(self.excel(excel_path))

    @staticmethod
    def isDecryptedExcelFile(excel_path):
        return isExcel(excel_path)

    def copyAndEncryptExampleExcel(self):
        data = self.excel(UserFilesPath.example_excel)
        self.saveExcel(data)

    def saveExcel(
        self,
        data: Union[bytes, pandas.core.frame.DataFrame],
        name: str = None,
        to_encode=True,
    ):
        """
        Save the excel into the user's data folder.
        name: Used to name the excel, 'expenses' by default
        """

        def convertDataframeToBytes(dataframe):
            buffer = io.BytesIO()
            with pandas.ExcelWriter(buffer) as writer:
                dataframe.to_excel(writer)
                writer.save()
            buffer.seek(0)
            file_data = buffer.read()
            return file_data

        if name is not None:
            file_path = FilePath.formPathUsing(
                self.user_files_path.user_folder, name + ".xlsx"
            )
        else:
            file_path = self.user_files_path.excel

        if type(data) == pandas.core.frame.DataFrame:
            data = convertDataframeToBytes(data)

        if to_encode == True:
            encrypted_data = self.fernet_encryption.encryptData(data)
        else:
            encrypted_data = data
        self.writeBinary(file_path, encrypted_data)

    def removeExcel(self):
        self.removeFile(self.user_files_path.excel)

    @property
    def intelligent_fill(self):
        return self.dataOfJson(self.user_files_path.intelligent_fill)

    def updateIntelligentFill(self, data: dict):
        self.writeJson(self.user_files_path.intelligent_fill, data)

    @property
    def categories(self):
        return self.dataOfJson(self.user_files_path.categories)

    def updateCategories(self, data: dict):
        return self.writeJson(self.user_files_path.categories, data)

    @property
    def translations(self):
        return self.dataOfJson(self.user_files_path.translations)

    @property
    def equivalent_columns(self):
        return self.dataOfJson(self.user_files_path.translations)["equivalent_columns"]

    def updateTranslations(self, data: dict):
        return self.writeJson(self.user_files_path.translations, data)

    @property
    def equivalent_columns(self):
        return self.translations["equivalent_columns"]


# TODO: handle concurrency on writing root convert company in category
#       by doing a Lock


class FernetEncryption:
    """Encryption logic that can be used on any document.
    It needs a private key to protect the data."""

    def __init__(self, key):
        self.fernet = Fernet(key)

    def generateKey(self, path_new_key):
        key = self.fernet.generate_key()
        with open(path_new_key, "wb") as key_file:
            key_file.write(key)

    def encryptData(self, file_data):
        encrypted_data = self.fernet.encrypt(file_data)
        return encrypted_data

    def decryptData(self, encrypted_data):
        file_data = self.fernet.decrypt(encrypted_data)
        return file_data


# class AccessNotebookConfig(FileAccessor):
#     """CRUD operations on the notebook confs of the application"""

#     # TODO: change this to for each user + save
#     def __init__(self):
#         self.NotebookConfigPath = NotebookConfigPath()

#     def getJson(self):
#         data = {}
#         with open(self.NotebookConfigPath.getNotebookConfigPath(), "r") as json_file:
#             data = json.load(json_file)
#         return data

#     def writeJson(self, data):
#         with open(self.NotebookConfigPath.getNotebookConfigPath(), "w") as json_file:
#             try:
#                 json.dump(data, json_file, indent=4)
#             except TypeError:
#                 logging.exception("JSON of wrong type :\n", data)

#     def getPrettyJson(self):
#         data = self.getJson()
#         json_formatted_str = json.dumps(data, indent=4)
#         return json_formatted_str


# class AccessStandardButtonsConfig(FileAccessor):
#     """CRUD operations on the button confs of the application"""

#     # TODO: change this to for each user + save
#     def __init__(self):
#         self.StandardButtonsConfigPath = StandardButtonsConfigPath()

#     def getJson(self):
#         data = {}
#         with open(
#             self.StandardButtonsConfigPath.getStandardButtonsConfigPath(), "r"
#         ) as json_file:
#             data = json.load(json_file)
#         return data

#     def writeJson(self, data):
#         with open(
#             self.StandardButtonsConfigPath.getStandardButtonsConfigPath(), "w"
#         ) as json_file:
#             try:
#                 json.dump(data, json_file, indent=4)
#             except TypeError:
#                 logging.exception("JSON of wrong type :\n", data)

#     def getPrettyJson(self):
#         data = self.getJson()
#         json_formatted_str = json.dumps(data, indent=4)
#         return json_formatted_str


class UnittestFilesAccess(FileAccessor):
    """CRUD operations on the unittest files"""

    @classproperty
    def pipeline_test_values(cls):
        return [
            (pandas.read_excel(input_file), cls.dataOfJson(output_file))
            for input_file, output_file in UnittestFilesPath.pipeline_test_values
        ]

    @classproperty
    def convert_test_values(cls):
        return [
            (pandas.read_excel(input_file), cls.dataOf(output_file).split("\n"))
            for input_file, output_file in UnittestFilesPath.convert_test_values
        ]
