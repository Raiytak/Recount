# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This file aims to do the CRUD manipulations on the files used by the application.
The paths used are stored in the paths_docs module, and are used by the wrappers of this module.
"""

"""ACHTUNG: To access user files, you should always do it using AccessUserFiles class !"""


import shutil
import json
import os

from .path_files import *

from cryptography.fernet import Fernet


def is_excel(path_file):
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
        with open(path_file, "rb") as file:
            file.seek(offset, whence)  # Seek to the offset.
            bytes = file.read(size)  # Capture the specified number of bytes.
            if bytes == sig:
                return True
    return False


class AccessorFile:
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
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def writeJson(file_path: Path, data: dict):
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

    @staticmethod
    def removeFile(path_file):
        if FilePath.pathExists(path_file):
            os.remove(path_file)


class AccessConfig(AccessorFile):
    """CRUD operations on the config files of the application"""

    @classproperty
    def databaseConfig(cls):
        stage = os.getenv("RECOUNT_STAGE")
        app_configs = cls.appConfigs
        db_configs = app_configs[stage]["mysql"]
        return db_configs

    @classproperty
    def appConfigs(cls):
        with open(ConfigPath.applicationConfigs, "r") as json_file:
            data = json.load(json_file)
        return data

    @classproperty
    def excelKey(cls):
        return cls.dataOfBinary(ConfigPath.excelKey)

    @classproperty
    def sqlKey(cls):
        return cls.dataOfBinary(ConfigPath.sqlKey)

    @classproperty
    def users(cls):
        return cls.dataOfJson(ConfigPath.users)

    # TODO 5155: add SSL context
    @classproperty
    def sslContext(cls):
        cert_file = ConfigPath.certificate
        private_key_file = ConfigPath.privateKey
        return (cert_file, private_key_file)


class AccessUserFiles(AccessorFile):
    """CRUD operations on all the excels of the application"""

    def __init__(self, username: str = None):
        if username is None:
            self.user_files_path = UserFilesPath
        else:
            self.user_files_path = UserFilesPath(username)
            self.initializeUserFolders()

        self.fernet_encryption = FernetEncryption(AccessConfig.excelKey)

    def initializeUserFolders(self):
        if not FilePath.pathExists(self.user_files_path.userFolder):
            self.createUserFolder()
        if not FilePath.pathExists(self.user_files_path.excel):
            self.copyExampleExcel()

    def createUserFolder(self):
        os.mkdir(self.user_files_path.userFolder)

    def removeUserFolder(self):
        if FilePath.pathExists(self.user_files_path.userFolder):
            shutil.rmtree(self.user_files_path.userFolder, ignore_errors=False)

    def excel(self, excel_path: Path = None):
        """If no path is provided, gets the 'expenses.xlsx' of the selected
        user, or the example one if no user is given"""
        if excel_path is None:
            excel_path = self.user_files_path.excel
        is_excel = self.isDecryptedExcelFile(excel_path)
        if is_excel == True:
            return self.dataOfBinary(excel_path)
        elif is_excel == False:
            encrypted_data = self.dataOfBinary(excel_path)
            return self.fernet_encryption.decryptData(encrypted_data)

    @staticmethod
    def isDecryptedExcelFile(excel_path):
        return is_excel(excel_path)

    def copyExampleExcel(self):
        shutil.copyfile(UserFilesPath.exampleExcel, self.user_files_path.excel)

    def saveExcel(self, data, name: str = None, to_encode=True):
        if name is not None:
            file_path = FilePath.formPathUsing(self.user_files_path.excelFolder, name)
        else:
            file_path = self.user_files_path.excel

        if to_encode == True:
            encrypted_data = self.fernet_encryption.encryptData(data)
        else:
            encrypted_data = data
        self.writeBinary(file_path, encrypted_data)

    def removeExcel(self):
        self.removeFile(self.user_files_path.excel)

    # TODO 7737: change this to for each user + save
    @property
    def descriptionToCategory(self):
        return self.dataOfJson(self.user_files_path.descriptionToCategory)

    # TODO 7737: change this to for each user + save
    def updateDescriptionToCategory(self, data: dict):
        self.writeJson(self.user_files_path.descriptionToCategory, data)

    # TODO 7737: change this to for each user + save
    @property
    def categoriesAuthorized(self):
        return self.dataOfJson(self.user_files_path.categoriesAuthorized)

    # TODO 7737: change this to for each user + save
    def updateCategoriesAuthorized(self, data: dict):
        return self.writeJson(self.user_files_path.categoriesAuthorized, data)


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


# class AccessNotebookConfig(AccessorFile):
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


# class AccessStandardButtonsConfig(AccessorFile):
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
