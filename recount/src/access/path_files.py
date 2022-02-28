# -*- coding: utf-8 -*-
"""
                    ====     DESCRIPTION    ====
This file contains the paths of the documents used in the app.
The manipulations of those files are done in other access_files or in the
class directly.
"""

"""ACHTUNG: To access user files, you should always do it using UserFilesAccess class !"""


from argparse import ArgumentError
import os
import sys
import re
from pathlib import Path
from enum import Enum
import abc
from datetime import date
from typing import Union, List

from recount_tools import classproperty


# ROOT PATH of the project detected using the path from which the application is launched
def rootPath():
    root_path = os.path.abspath(__file__)
    app_path = Path(re.sub("(recount).*", "", root_path))
    return app_path


ROOT_PATH = rootPath()
APP_PATH = ROOT_PATH / "recount"
STR_APP_PATH = str(APP_PATH)
if STR_APP_PATH not in sys.path:
    sys.path.insert(0, STR_APP_PATH)


class Folder(Enum):
    SOURCE = "src"
    DATA = "data"

    CONFIG = "config"
    USERS = "users"
    GLOBAL = "global"
    EXAMPLE = "examples"

    EXCELS = "excels"
    VUES = "vues"
    LOGS = "logs"

    # CATEGORIES = "categories"
    # INTELLIGENT_FILL = "intelligent_fill"
    # STANDARD_BUTTONS = "standard_buttons"
    # NOTEBOOK_EXCEL = "notebook_excel"


class FilePath:
    """Hook methods to get the path of the files of the application"""

    @property
    @classmethod
    @abc.abstractmethod
    def root(self):
        """Root of the folder containing the desired files"""

    @staticmethod
    def pathExists(*folders_and_file: List[Union[str, Folder, Path]]):
        file_path = FilePath.formPathUsing(*folders_and_file)
        bool_exists = os.path.exists(file_path)
        return bool_exists

    @staticmethod
    def formPathUsing(*folders_and_file: List[Union[str, Folder, Path]]) -> Path:
        if None in folders_and_file:
            raise ArgumentError(
                f"None has been passed as argument in '{folders_and_file}'"
            )
        complete_path = folders_and_file[0]
        for name in folders_and_file[1:]:
            if type(name) is Folder:
                name = name.value
            if name != ():
                complete_path = complete_path / name
        return complete_path


class ConfigPath(FilePath):
    """Path to the configs containing all the secrets of the application :
        -private keys that encrypt / decrypt the excels
        -users name and password
        -server certificates"""

    root = FilePath.formPathUsing(APP_PATH, Folder.CONFIG)

    @classproperty
    def application(cls):
        return cls.formPathUsing(cls.root, "app_configs.json")

    @classproperty
    def users(cls):
        return cls.formPathUsing(cls.root, "users.json")

    @classproperty
    def currencies(cls):
        return cls.formPathUsing(cls.root, "currencies.json")

    @classproperty
    def currencies_rates_filenames(cls):
        filenames = [
            filename for filename in os.listdir(cls.root) if filename.startswith("ecb_")
        ]
        return filenames

    @classproperty
    def currencies_rates(cls):
        filenames = cls.currencies_rates_filenames
        if len(filenames) == 0:
            filename = cls.today_currencies_rates_filename
        else:
            filename = filenames[0]
        return cls.formPathUsing(cls.root, filename)

    @classproperty
    def today_currencies_rates_filename(cls):
        return f"ecb_{date.today():%Y%m%d}.zip"

    @classproperty
    def excel_key(cls):
        return cls.formPathUsing(cls.root, "keys", "excel.key")

    @classproperty
    def sql_ey(cls):
        return cls.formPathUsing(cls.root, "keys", "data_sql.key")

    # @classproperty
    # def certificate(cls):  # TODO : Add certificates
    #     return cls.formPathUsing(cls.root, "keys", "other-csr.pem")
    #     path_exists, path_created = cls.pathExists(filename="other-csr.pem")
    #     if path_exists:
    #         return path_created
    #     else:
    #         path_exists, path_created = cls.pathExists(filename="server-csr.pem")
    #         return cls.formPathUsing(cls.PathInformation)

    # @classproperty
    # def privateKey(cls):  # TODO : Add keys
    #     list_folders = ["", "keys"]
    #     path_exists, path_created = cls.pathExists(
    #         list_folders, "other-private-key.pem"
    #     )
    #     if path_exists:
    #         return path_created
    #     else:
    #         path_exists, path_created = cls.pathExists(
    #             list_folders, "server-private-key.pem"
    #         )
    #         return path_created


class LogPath(FilePath):
    """Path to the logs of the application"""

    root = FilePath.formPathUsing(APP_PATH, Folder.SOURCE, Folder.LOGS)

    @classproperty
    def application(cls):
        return cls.formPathUsing(cls.root, "application.log")

    @classproperty
    def db_com(cls):
        return cls.formPathUsing(cls.root, "db_com.log")

    @classproperty
    def error(cls):
        return cls.formPathUsing(cls.root, "error.log")

    @classproperty
    def logs_path(cls):
        paths = [
            getattr(LogPath, name)
            for name in cls.__dict__.keys()
            if not name.startswith("_") and name != "root" and name != "logs_path"
        ]
        return paths


class UserFilesPath(FilePath):
    """Path to the excels used :
        -source excel (from the user (saved / imported) or from the folder examples)
        -copy excel (copy of the source excel, cleaned and
                    manipulated by the application, then removed)
        If reaching users' file, 'root' should be the excel's user folder"""

    root = FilePath.formPathUsing(APP_PATH, Folder.EXAMPLE)

    def __init__(self, username: str = None):
        if username is not None:
            self.username = username
            self.root = self.user_folder

    @property
    def user_folder(self):
        return FilePath.formPathUsing(
            ROOT_PATH, Folder.DATA, Folder.USERS, self.username
        )

    @property
    def excel(self):
        return self.formPathUsing(self.root, "expenses.xlsx")

    @property
    def categories(self):
        return self.formPathUsing(self.root, "categories.json")

    @property
    def intelligent_fill(self):
        return self.formPathUsing(self.root, "intelligent_fill.json")

    @property
    def translations(self):
        return self.formPathUsing(self.root, "user_translations.json")

    @classproperty
    def example_excel(cls):
        return cls.formPathUsing(cls.root, "example_expenses_en.xlsx")

    @classproperty
    def example_categories(cls):
        return cls.formPathUsing(cls.root, "example_categories.json")

    @classproperty
    def example_intelligent_fill(cls):
        return cls.formPathUsing(cls.root, "example_intelligent_fill.json")

    @classproperty
    def example_translations(cls):
        return cls.formPathUsing(cls.root, "example_translations.json")


#     def getNotebookConfigPath(self):
#         self.PathInformation.folders = [self.notebook_excel]
#         self.PathInformation.filename = "categories_themes_authorized_test.json"
#         return self.formPathUsing(self.PathInformation)


# @property
#     def getStandardButtonsConfigPath(self):
#         self.PathInformation.folders = [self.vues_folder, self.standard_buttons]
#         self.PathInformation.filename = "config_buttons.json"
#         return self.formPathUsing(self.PathInformation)


class UnittestFilesPath(FilePath):
    """Path to the files used by the unittests"""

    root = FilePath.formPathUsing(APP_PATH, "unittests", "test_files")

    @classproperty
    def folder(cls):
        return cls.root

    @classproperty
    def pipeline_test_values(cls):
        """Returns the paired input output files for the tests of pipeline"""
        input_files = [
            path
            for path in cls.root.iterdir()
            if path.is_file() and ("excel_input" in path.stem)
        ]
        output_files = [
            path
            for path in cls.root.iterdir()
            if path.is_file() and ("pipeline_output" in path.stem)
        ]

        paired_test_files = []
        for input_file in input_files:
            filename = input_file.stem
            number = filename.split("_")[-1]

            output_file = next(
                output_file
                for output_file in output_files
                if number in output_file.stem
            )
            paired_test_files.append([input_file, output_file])
        return paired_test_files

    # TODO
    @classproperty
    def convert_test_values(cls):
        """Returns the paired input output files for the tests of convert"""
        input_files = [
            path
            for path in cls.root.iterdir()
            if path.is_file() and ("excel_input" in path.stem)
        ]
        output_files = [
            path
            for path in cls.root.iterdir()
            if path.is_file() and ("convert_output" in path.stem)
        ]

        paired_test_files = []
        for input_file in input_files:
            filename = input_file.stem
            number = filename.split("_")[-1]

            output_file = next(
                output_file
                for output_file in output_files
                if number in output_file.stem
            )
            paired_test_files.append([input_file, output_file])
        return paired_test_files

    @classmethod
    def getInputFileNumber(cls, number):
        return next(
            [
                path
                for path in cls.root.iterdir()
                if path.is_file()
                and ("excel_input" in path.stem)
                and (number in path.stem)
            ]
        )

    @classmethod
    def getOutputFileNumber(cls, number):
        return next(
            [
                path
                for path in cls.root.iterdir()
                if path.is_file()
                and ("pipeline_output" in path.stem)
                and (number in path.stem)
            ]
        )

