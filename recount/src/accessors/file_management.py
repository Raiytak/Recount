# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This file aims to do the CRUD manipulations on the files used by the application.
The paths used are stored in the paths_docs module, and are used by the wrappers of this module.
"""

"""ACHTUNG: To access user files, you should always do it using UserFolder class !"""


import abc
import typing
import os
from pathlib import Path
import io
import json
import shutil
import pandas


import path_definition
import encryption

__all__ = [
    "RootFolder",
    "AssetFolder",
    "LogFolder",
    "DataFolder",
    "ConfigFolder",
    "UsersFolder",
    "KeyFolder",
    "KeyManager",
    "UserManager",
    "Config",
]


class FileAccessor:
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
    def removeFile(filepath):
        if filepath.exists():
            os.remove(filepath)


class _Excel:
    @staticmethod
    def isExcel(filepath) -> bool:
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
            with open(filepath, "rb") as file:
                file.seek(offset, whence)  # Seek to the offset.
                bytes = file.read(size)  # Capture the specified number of bytes.
                if bytes == sig:
                    return True
        return False


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
        example_sql_conf = path_definition.ConfigFolder.DEFAULT_SQL
        shutil.copy2(src=example_sql_conf, dst=cls.SQL_PATH)

    @classmethod
    def copyExampleConfig(cls):
        cls.copyExampleSqlConfig()


class Config:
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


class LogFolder(FolderManager):
    ROOT = path_definition.LogFolder.ROOT

    @staticmethod
    def clearLogs():
        for log_path in path_definition.LogFolder:
            FileAccessor.removeFile(log_path)


class UsersFolder(FolderManager):
    ROOT = path_definition.UsersFolder.ROOT

    @property
    def isEmpty(self) -> bool:
        return [file for file in os.listdir(self.ROOT)] == []

    @staticmethod
    def convertDataframeToBytes(dataframe):
        buffer = io.BytesIO()
        with pandas.ExcelWriter(buffer) as writer:
            dataframe.to_excel(writer)
            writer.save()
        buffer.seek(0)
        file_data = buffer.read()
        return file_data


# =====================================================================================
# ================================= PUBLIC API ========================================
# =====================================================================================


class KeyManager:
    _ROOT = KeyFolder.ROOT
    DEFAULT_EXCEL_KEY_NAME = path_definition.KeyFolder.DEFAULT_EXCEL_KEY_NAME
    DEFAULT_EXCEL_KEY = _ROOT / DEFAULT_EXCEL_KEY_NAME

    @property
    def ROOT(self) -> typing.Type[Path]:
        return self._ROOT

    def get(self, key_name: str):
        return FileAccessor.readBinary(self.ROOT / key_name)

    def set(self, key_name: str, key: bytes):
        return FileAccessor.writeBinary(self.ROOT / key_name, key)

    def getDefaultExcelKey(self):
        return self.get(self.DEFAULT_EXCEL_KEY_NAME)

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


class UserManager:
    """CRUD operations on the files of the defined user"""

    def __init__(self, username: str = "", key: typing.Union[bytes, str] = ""):
        if not username:
            self._username = "default"
        else:
            self._username = username
        self._ROOT = path_definition.UsersFolder.ROOT / self.username

        # Instanciation of a file encryption object
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

    def excel(self, filepath: Path = None) -> bytes:
        """Return the data of 'filepath'
        If no path is provided, default excel data is returned"""

        if not filepath:
            filepath = self.default_excel_path

        if not filepath.exists():
            raise FileNotFoundError(
                "The file '{}' does not exists".format(str(filepath))
            )

        if filepath.suffix != "xlsx":
            raise AttributeError(
                "The file provided is '{}' where it is expected to be a 'xlsx'".format()
            )

        unknown_data = FileAccessor.readBinary(filepath)
        if not _Excel.isExcel(filepath):
            decrypted_data = self.file_encryption.decryptData(unknown_data)
            if not _Excel.isExcel(decrypted_data):
                # Case 3: Either the decryption did not work or the file is not an excel
                raise ValueError(
                    "The provided file '{}' is either not an excel or is encrypted with a different from the one used by the user '{}'".format(
                        filepath, self.username
                    )
                )
            else:
                # Case 1: The file provided was encrypted, decryption worked out
                data = decrypted_data
        else:
            # Case 2: The file provided was already clear
            data = unknown_data
        return data

    def dataframe(self, filepath: Path = None):
        """Returns the df of the file 'filepath'
        If not path is provided, return the df of the default excel"""
        df = pandas.read_excel(self.excel(filepath))
        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def saveExcel(
        self,
        data: typing.Union[bytes, pandas.core.frame.DataFrame],
        name: str = None,
        to_encode: bool = True,
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

        if type(data) == pandas.core.frame.DataFrame:
            data = _Excel.convertDataframeToBytes(data)

        if to_encode == True:
            data_to_write = self.file_encryption.encryptData(data)
        else:
            data_to_write = data
        FileAccessor.writeBinary(filepath, data_to_write)

    def removeDefaultExcel(self):
        FileAccessor.removeFile(self.default_excel_path)

    def removeAllExcels(self):
        for filepath in os.listdir(self.ROOT):
            FileAccessor.removeFile(filepath)


# def saveUploadedFile(self, file_uploaded):
#     content_type_encoded, content_string_encoded = file_uploaded.split(",")
#     content_decoded = self.getTypeAndDecodeUploadedFile(content_string_encoded)
#     file_data = content_decoded.read()
#     self.saveExcel(file_data)

# @staticmethod
# def getTypeAndDecodeUploadedFile(content_string_encoded):
#     # if any(["xml" in content_type_encoded) or ("xls" in content_type_encoded) :
#     #     content_decoded = io.BytesIO(content_string_base64)
#     # else:
#     #     raise TypeError("Uploaded file is expected to be created from openxml or excel")
#     content_string_base64 = base64.b64decode(content_string_encoded)
#     content_decoded = io.BytesIO(content_string_base64)
#     return content_decoded

# @property
# def intelligent_fill(self):
#     return self.readJson(self.user_files_path.intelligent_fill)

# def updateIntelligentFill(self, data: dict):
#     self.writeJson(self.user_files_path.intelligent_fill, data)

# @property
# def categories(self):
#     return self.readJson(self.user_files_path.categories)

# def updateCategories(self, data: dict):
#     return self.writeJson(self.user_files_path.categories, data)

# @property
# def translations(self):
#     return self.readJson(self.user_files_path.translations)

# def updateTranslations(self, data: dict):
#     return self.writeJson(self.user_files_path.translations, data)

# @property
# def equivalent_columns(self):
#     return self.translations["equivalent_columns"]


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


# class UnittestFiles:
#     """CRUD operations on the unittest files"""

#     pipeline_test_values = [
#         (pandas.read_excel(input_file), FileAccessor.readJson(output_file))
#         for input_file, output_file in UnittestFilesPath.pipeline_test_values
#     ]

#     convert_df_to_sql_test_values = [
#         (pandas.read_excel(input_file), FileAccessor.read(output_file).split("\n"))
#         for input_file, output_file in UnittestFilesPath.convert_df_to_sql_test_values
#     ]
