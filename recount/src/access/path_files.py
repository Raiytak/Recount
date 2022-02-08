# -*- coding: utf-8 -*-
"""
                    ====     DESCRIPTION    ====
This file contains the paths of the documents used in the app.
The manipulations of those files are done in other access_files or in the
class directly.
"""

"""ACHTUNG: To access user files, you should always do it using AccessUserFiles class !"""


from argparse import ArgumentError
import os
import sys
import re
from pathlib import Path
from enum import Enum
import abc
from typing import Union, List


class ClassPropertyDescriptor(object):
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self

    def getter(self, func):
        return func()


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


# ROOT PATH of the project detected using the path from which the application is launched
def getAppPath():
    root_path = os.path.abspath(__file__)
    app_path = Path(re.sub("(recount).*", "recount", root_path))
    return app_path


APP_PATH = getAppPath()
if APP_PATH not in sys.path:
    sys.path = [APP_PATH] + sys.path


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
        path_file = FilePath.formPathUsing(*folders_and_file)
        bool_exists = os.path.exists(path_file)
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

    root = FilePath.formPathUsing(APP_PATH, Folder.SOURCE, Folder.CONFIG)

    @classproperty
    def application(cls):
        return cls.formPathUsing(cls.root, "app_configs.json")

    @classproperty
    def users(cls):
        return cls.formPathUsing(cls.root, "users.json")

    @classproperty
    def excelKey(cls):
        return cls.formPathUsing(cls.root, "keys", "excel.key")

    @classproperty
    def sqlKey(cls):
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

    root = FilePath.formPathUsing(APP_PATH, Folder.DATA, Folder.EXAMPLE)

    def __init__(self, username: str = None):
        if username is not None:
            self.username = username
            self.root = self.userFolder

    @property
    def userFolder(self):
        return FilePath.formPathUsing(
            APP_PATH, Folder.DATA, Folder.USERS, self.username
        )

    @property
    def excel(self):
        return self.formPathUsing(self.root, "expenses.xlsx")

    @property
    def excelFolder(self):
        return self.root

    @classproperty
    def exampleExcel(cls):
        return cls.formPathUsing(cls.root, "example_expenses_en.xlsx")

    # TODO 7737: change this to for each user + save
    @property
    def categoriesAuthorized(self):
        return self.formPathUsing(
            APP_PATH, Folder.DATA, Folder.GLOBAL, "categories_themes_authorized.json"
        )

    # TODO 7737: change this to for each user + save
    @property
    def descriptionToCategory(self):
        return self.formPathUsing(
            APP_PATH, Folder.DATA, Folder.GLOBAL, "convert_descr_to_theme.json"
        )


#     def getNotebookConfigPath(self):
#         self.PathInformation.folders = [self.notebook_excel]
#         self.PathInformation.filename = "categories_themes_authorized_test.json"
#         return self.formPathUsing(self.PathInformation)


# @property
#     def getStandardButtonsConfigPath(self):
#         self.PathInformation.folders = [self.vues_folder, self.standard_buttons]
#         self.PathInformation.filename = "config_buttons.json"
#         return self.formPathUsing(self.PathInformation)
