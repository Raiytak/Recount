# -*- coding: utf-8 -*-
""" 
CRUD manipulations on the files used by the application.
The paths used are stored in the path_definition.py file,
"""


import abc
import typing
import os
from pathlib import Path
import json
import shutil
import pickle

# import pandas as pd


import path_definition
import encryption

__all__ = [
    "RootFolder",
    "AssetFolder",
    "LogFolder",
    "DataFolder",
    "ConfigFolder",
    "LoginFolder",
    "UsersFolder",
    "KeyFolder",
    #############
    # Pubic API #
    #############
    "AssetManager",
    "LogManager",
    "KeyManager",
    "UserManager",
    "ConfigManager",
    "LoginManager",
]


class FileAccessor:
    @staticmethod
    def read(filepath: Path) -> bytes:
        with open(filepath, "r") as file:
            data = file.read()
        return data

    @staticmethod
    def write(filepath: Path, data: bytes):
        with open(filepath, "w") as file:
            file.write(data)

    @staticmethod
    def pickleLoad(filepath: Path) -> bytes:
        with open(filepath, "rb") as file:
            data = pickle.load(file)
        return data

    @staticmethod
    def pickleDump(filepath: Path, data: bytes):
        with open(filepath, "wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def readBinary(filepath: Path) -> bytes:
        with open(filepath, "rb") as file:
            data = file.read()
        return data

    @staticmethod
    def writeBinary(filepath: Path, data: bytes):
        with open(filepath, "wb") as file:
            file.write(data)

    @staticmethod
    def readJson(filepath: Path):
        with open(filepath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def writeJson(filepath: Path, data: dict):
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def removeFile(filepath: Path):
        if filepath.exists():
            os.remove(filepath)


class _Excel:
    @staticmethod
    def isExcel(filepath: Path = None, data_bytes: bytes = None) -> bool:
        if filepath and data_bytes:
            raise AttributeError("filpath and data_bytes provided at the same time")
        # TODO 2496: use openpyxl instead
        accepted_excel_signatures = [
            (b"\x50\x4B\x05\x06", 2, -22, 4),
            (b"\x09\x08\x10\x00\x00\x06\x05\x00", 0, 512, 8),  # Saved from _Excel
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
            ),  # Saved from _Excel then saved from Calc
        ]

        for sig, whence, offset, size in accepted_excel_signatures:
            if filepath:
                with open(filepath, "rb") as file:
                    file.seek(offset, whence)  # Seek to the offset.
                    data_bytes = file.read(
                        size
                    )  # Capture the specified number of bytes.
            if data_bytes == sig[offset:size]:
                return True
        return False

        # for sig, whence, offset, size in accepted_excel_signatures:
        #     with open(filepath, "rb") as file:
        #         file.seek(offset, whence)  # Seek to the offset.
        #         data_bytes = file.read(size)  # Capture the specified number of bytes.
        #         if data_bytes == sig:
        #             return True
        # return False


class FolderManager:
    @property
    @abc.abstractmethod
    def ROOT(self) -> Path:
        """Root path of the Folder"""
        # TODO: automate instanciation

    @classmethod
    def createFolder(cls):
        if not cls.folderExists():
            os.mkdir(cls.ROOT)

    @classmethod
    def removeFolder(cls):
        shutil.rmtree(cls.ROOT)

    @classmethod
    def folderExists(cls) -> bool:
        return cls.ROOT.exists()


class RootFolder(FolderManager):
    ROOT = path_definition.RootFolder.ROOT


class DataFolder(FolderManager):
    ROOT = path_definition.DataFolder.ROOT


class AssetFolder(FolderManager):
    ROOT = path_definition.AssetFolder.ROOT

    @classmethod
    def copyDefaultAssets(cls):
        path_default_assets = path_definition.AssetFolder.DEFAULT
        for filename in os.listdir(path_default_assets):
            filepath = path_default_assets / filename
            if os.path.isfile(filepath):
                shutil.copy2(filepath, cls.ROOT)


class KeyFolder(FolderManager):
    ROOT = path_definition.KeyFolder.ROOT


class ConfigFolder(FolderManager):
    ROOT = path_definition.ConfigFolder.ROOT
    SQL_PATH = path_definition.ConfigFolder.SQL_PATH

    @classmethod
    def copyExampleSqlConfig(cls):
        example_sql_conf = path_definition.ExampleFolder.SQL_CONFIG
        shutil.copy2(src=example_sql_conf, dst=cls.SQL_PATH)

    @classmethod
    def copyExampleConfig(cls):
        cls.copyExampleSqlConfig()


class LoginFolder(FolderManager):
    ROOT = path_definition.LoginFolder.ROOT
    LOGIN_FILE = path_definition.LoginFolder.LOGIN_FILE


class LogFolder(FolderManager):
    ROOT = path_definition.LogFolder.ROOT
    APP = path_definition.LogFolder.APP
    APP_ERROR = path_definition.LogFolder.APP_ERROR
    SQL = path_definition.LogFolder.SQL

    @staticmethod
    def clearLogs():
        for log_path in path_definition.LogFolder:
            FileAccessor.removeFile(log_path)


class UsersFolder(FolderManager):
    ROOT = path_definition.UsersFolder.ROOT

    @property
    def isEmpty(self) -> bool:
        return [file for file in os.listdir(self.ROOT)] == []


# =====================================================================================
# ================================= PUBLIC API ========================================
# =====================================================================================


class FileManager:
    @property
    def ROOT(self) -> typing.Type[Path]:
        return self._ROOT


class AssetManager(FileManager):
    ROOT = AssetFolder.ROOT


class LogManager(FileManager):
    _ROOT = LogFolder.ROOT

    @classmethod
    def clearLogs(cls):
        for filename in os.listdir(cls._ROOT):
            filepath = cls._ROOT / filename
            os.remove(filepath)


class ConfigManager:
    ROOT = ConfigFolder.ROOT
    SQL = ConfigFolder.SQL_PATH

    @classmethod
    def sql(cls):
        data = FileAccessor.readJson(cls.SQL)
        return data

    @classmethod
    def setSqlAdminPassword(cls, password: str):
        data = FileAccessor.readJson(cls.SQL)
        data["password"] = password
        FileAccessor.writeJson(cls.SQL, data)


class LoginManager(FileManager):
    ROOT = LoginFolder.ROOT
    LOGIN_FILE = LoginFolder.LOGIN_FILE

    @classmethod
    def getUsers(cls) -> list:
        users_passwords = cls.getUsersAndPasswords()
        return users_passwords.keys()

    @classmethod
    def getUsersAndPasswords(cls) -> dict:
        users_passwords = FileAccessor.readJson(cls.LOGIN_FILE)
        return users_passwords

    @classmethod
    def copyExample(cls):
        shutil.copy(path_definition.ExampleFolder.LOGIN, cls.LOGIN_FILE)


class KeyManager(FileManager):
    _ROOT = KeyFolder.ROOT
    _DEFAULT_EXCEL_KEY_NAME = path_definition.KeyFolder._DEFAULT_EXCEL_KEY_NAME
    _DEFAULT_EXCEL_KEY = _ROOT / _DEFAULT_EXCEL_KEY_NAME

    def get(self, key_name: str):
        return FileAccessor.readBinary(self.ROOT / key_name)

    def set(self, key_name: str, key: bytes):
        return FileAccessor.writeBinary(self.ROOT / key_name, key)

    def getDefaultExcelKey(self):
        return self.get(self._DEFAULT_EXCEL_KEY_NAME)

    def generateKey(self, name: str, dirpath: Path = None, override: bool = False):
        """If dirpath is not specified, register the key in the default 'key' folder of Recount"""
        if not dirpath:
            key_path = self.ROOT / name
        else:
            key_path = dirpath / name
        if key_path.exists() and not override:
            raise FileExistsError("The key '{}' already exists".format(name))
        else:
            key = encryption.generateKey()
            FileAccessor.writeBinary(key_path, key)


class UserManager(FolderManager, FileManager):
    """CRUD operations on the files of the defined user"""

    EXAMPLE_EXCEL = path_definition.ExampleFolder.EXCEL_PATH

    def __init__(self, username: str = "", key: typing.Union[bytes, str] = None):
        if not username:
            self._username = "default"
        else:
            self._username = username
        self._ROOT = path_definition.UsersFolder.ROOT / self.username

        if not key:
            key_manager = KeyManager()
            key = key_manager.getDefaultExcelKey()
        self.file_encryption = encryption.FileEncryption(key)
        self.default_excel_path = (
            self.ROOT / path_definition.UsersFolder.DEFAULT_EXCEL_NAME
        )

    @property
    def username(self) -> str:
        return self._username

    @property
    def ROOT(self) -> typing.Type[Path]:
        return self._ROOT

    def createFolder(self):
        if not self.folderExists():
            os.mkdir(self.ROOT)

    def removeFolder(self):
        shutil.rmtree(self.ROOT)

    def folderExists(self) -> bool:
        return self.ROOT.exists()

    def excel(self, filepath: Path = None, filename: str = None) -> bytes:
        """Return the data of an excel
        If a filename is provided, returns the excel of the user named accordingly
        If filepath is not provided, default excel data is returned
        filename and filepath should not be provided at the same time"""
        if filename and filepath:
            raise AttributeError(
                "provided both filepath and filename, while the function expects only one argument"
            )
        if filename:
            filepath = self.ROOT / filename
        elif not filepath:
            filepath = self.default_excel_path

        if not filepath.exists():
            raise FileNotFoundError(
                "The file '{}' does not exists".format(str(filepath))
            )

        if filepath.suffix != ".xlsx":
            raise AttributeError(
                "The file provided is '{}' where it is expected to be a 'xlsx'".format(
                    filepath.suffix
                )
            )

        unknown_data = FileAccessor.readBinary(filepath)
        if not _Excel.isExcel(filepath=filepath):
            decrypted_data = self.file_encryption.decryptData(unknown_data)
            # TODO: isExcel not working on decrypted excel :/
            # if not _Excel.isExcel(data_bytes=decrypted_data):
            #     # Case 3: Either the decryption did not work (wrong key?) or the file is not an excel, even though it has the right extension
            #     raise ValueError(
            #         "The provided file '{}' is either not an excel or is encrypted with a different from the one used by the user '{}'".format(
            #             filepath, self.username
            #         )
            #     )
            # else:
            #     # Case 1: The file provided was encrypted, decryption worked out
            data = decrypted_data
        else:
            # Case 2: The file provided was already clear
            data = unknown_data
        return data

    def saveExcel(
        self,
        data: bytes,
        name: str = None,
        encrypt: bool = True,
        override: bool = True,
    ):
        """
        Save the excel into the user's data folder.
        name: Used to name the excel.
        """

        # filepath instanciation
        if name:
            filepath = self.ROOT / name
        else:
            filepath = self.default_excel_path

        if not override and filepath.exists():
            raise FileExistsError(
                "The file '{}' already exists. Set override to 'True' if needed".format(
                    filepath
                )
            )

        if encrypt == True:
            data_to_write = self.file_encryption.encryptData(data)
        else:
            data_to_write = data
        FileAccessor.writeBinary(filepath, data_to_write)

    def copyExampleExcel(self):
        shutil.copy(path_definition.ExampleFolder.EXCEL_PATH, self.default_excel_path)

    def removeDefaultExcel(self):
        FileAccessor.removeFile(self.default_excel_path)

    def removeAllExcels(self):
        for filepath in os.listdir(self.ROOT):
            FileAccessor.removeFile(self.ROOT / filepath)


class TestManager(FileManager):
    _ROOT = path_definition.TestFolder.FILES

    EXCEL_1 = path_definition.TestFolder.EXCEL_1
    OUTPUT_JSON_1 = path_definition.TestFolder.OUTPUT_JSON_1
    OUTPUT_PIPELINE_JSON_1 = path_definition.TestFolder.OUTPUT_PIPELINE_JSON_1
    DATABASE_DATAFRAME_JSON_1 = path_definition.TestFolder.DATABASE_DATAFRAME_JSON_1
    DATABASE_SAVE_DATAFRAME_1 = path_definition.TestFolder.DATABASE_SAVE_DATAFRAME_1

