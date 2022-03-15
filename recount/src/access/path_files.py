# -*- coding: utf-8 -*-
"""
                    ====     DESCRIPTION    ====
This file contains the paths of the documents used in the app.
The manipulations of those files are done in other access_files or in the
class directly.
"""

"""ACHTUNG: To access user files, you should always do it using UserFilesAccess class !"""


from pathlib import Path
from enum import Enum
import abc
from datetime import date

from recount_tools import classproperty


def rootPath():
    root_path = Path().resolve()
    if "recount" not in [file_path.stem for file_path in root_path.iterdir()]:
        if "src" not in [file_path.stem for file_path in root_path.iterdir()]:
            raise FileNotFoundError(
                "Recount can only be launched where the .git folder is present or inside recount folder"
            )
        else:
            root_path = root_path.parent
    return root_path


ROOT_PATH = rootPath()
APP_PATH = ROOT_PATH / "recount"
STR_APP_PATH = str(APP_PATH)


class Folder(Enum):
    SOURCE = "src"
    DATA = "data"

    CONFIG = "config"
    USERS = "users"
    EXAMPLE = "examples"

    LOGS = "logs"

    TEST = "tests"

    # GLOBAL = "global"
    # VUES = "vues"
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


class ConfigPath(FilePath):
    """Path to the configs containing all the secrets of the application :
        -private keys that encrypt / decrypt the excels
        -users name and password
        -server certificates"""

    root = APP_PATH / Folder.CONFIG.value

    @classproperty
    def application(cls):
        application_path = cls.root / "app_configs.json"
        if application_path.exists():
            return application_path
        return cls.root / "default_configs.json"

    @classproperty
    def users(cls):
        return cls.root / "users.json"

    @classproperty
    def currencies(cls):
        return cls.root / "currencies.json"

    @classproperty
    def currencies_rates_filenames(cls):
        filenames = [
            filename for filename in cls.root.iterdir() if filename.startswith("ecb_")
        ]
        return filenames

    @classproperty
    def currencies_rates(cls):
        filenames = cls.currencies_rates_filenames
        if len(filenames) == 0:
            filename = cls.today_currencies_rates_filename
        else:
            filename = filenames[0]
        return cls.root / filename

    @classproperty
    def today_currencies_rates_filename(cls):
        return f"ecb_{date.today():%Y%m%d}.zip"

    @classproperty
    def excel_key(cls):
        return cls.root / "keys" / "excel.key"

    @classproperty
    def sql_ey(cls):
        return cls.root / "keys" / "data_sql.key"

    # @classproperty
    # def certificate(cls):  # TODO : Add certificates
    #     return cls.root / "keys" / "other-csr.pem"
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

    root = ROOT_PATH / Folder.LOGS.value

    @classproperty
    def application(cls):
        return cls.root / "application.log"

    @classproperty
    def db_com(cls):
        return cls.root / "db_com.log"

    @classproperty
    def error(cls):
        return cls.root / "error.log"

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

    root = APP_PATH / Folder.EXAMPLE.value

    def __init__(self, username: str = None):
        if username is not None:
            self.username = username
            self.root = self.user_folder

    @property
    def user_folder(self):
        return ROOT_PATH / Folder.DATA.value / Folder.USERS.value / self.username

    @property
    def excel(self):
        return self.root / "expenses.xlsx"

    @property
    def categories(self):
        return self.root / "categories.json"

    @property
    def intelligent_fill(self):
        return self.root / "intelligent_fill.json"

    @property
    def translations(self):
        return self.root / "user_translations.json"

    @classproperty
    def example_excel(cls):
        return cls.root / "example_expenses_en.xlsx"

    @classproperty
    def example_categories(cls):
        return cls.root / "example_categories.json"

    @classproperty
    def example_intelligent_fill(cls):
        return cls.root / "example_intelligent_fill.json"

    @classproperty
    def example_translations(cls):
        return cls.root / "example_translations.json"


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

    root = APP_PATH / Folder.TEST.value / "test_files"

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
    def convert_df_to_sql_test_values(cls):
        """Returns the paired input output files for the tests of convert"""
        input_files = [
            path
            for path in cls.root.iterdir()
            if path.is_file() and ("excel_input" in path.stem)
        ]
        output_files = [
            path
            for path in cls.root.iterdir()
            if path.is_file() and ("convert_df_to_sql_output" in path.stem)
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

