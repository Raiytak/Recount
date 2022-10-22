# -*- coding: utf-8 -*-
"""
                    ====     DESCRIPTION    ====
This file contains the paths of the documents used in the app.
The manipulations of those files are done in other access_files or in the
class directly.
"""

"""ACHTUNG: To access user files, you should always do it using UserFolder class !"""

# TODO rename file

from pathlib import Path
from enum import Enum

__all__ = ["RootFolder", "DataFolder", "LogFolder", "KeyFolder"]


class RootFolder(Enum):
    HOME = Path.home()
    ROOT = HOME / ".recount"

    ASSET = ROOT / "asset"
    CONFIG = ROOT / "config"
    DATA = ROOT / "data"
    KEY = ROOT / "key"
    LOGIN = ROOT / "login"
    LOG = ROOT / "log"


class DataFolder(Enum):
    ROOT = RootFolder.LOG.value


class LogFolder(Enum):
    ROOT = RootFolder.LOG.value
    APP = ROOT / "app.log"
    APP_ERROR = ROOT / "app_error.log"
    SQL = ROOT / "sql_communcation.log"


class UsersFolder(Enum):
    ROOT = RootFolder.DATA.value / "user"
    DEFAULT_EXCEL_NAME = "default.xlsx"


class KeyFolder(Enum):
    ROOT = RootFolder.KEY.value
    DEFAULT_EXCEL_KEY_NAME = "default_excel.key"


class Config(Enum):
    pass


# class AssetPath:
#     """Path to the folder containing the CSS rules and asset of the app"""

#     _ROOT = "/var/recount/asset"
#     ROOT = pathlib.Path(_ROOT) / Folder.ASSET.value


# class ConfigPath:
#     """Path to the configs containing all the secrets of the application :
#         -private keys that encrypt / decrypt the excels
#         -USERS name and password
#         -server certificates"""

#     _ROOT = "/etc/recount"
#     ROOT = pathlib.Path(_ROOT) / Folder.CONFIG.value

#     USERS = ROOT / "USERS.json"

#     CURRENCIES = ROOT / "CURRENCIES.json"  # TODO : put to assets

#     SQL_KEY = ROOT / "keys" / "data_sql.key"
#     EXCEL_KEY = ROOT / "keys" / "excel.key"

#     @classproperty
#     def application(cls):
#         application_path = cls.ROOT / "app_configs.json"
#         if application_path.exists():
#             return application_path
#         return cls.ROOT / "default_configs.json"

#     @classproperty
#     def currencies_rates_filenames(cls):
#         filenames = [
#             filename for filename in cls.ROOT.iterdir() if filename.startswith("ecb_")
#         ]
#         return filenames

#     @classproperty
#     def currencies_rates(cls):
#         filenames = cls.currencies_rates_filenames
#         if len(filenames) == 0:
#             filename = cls.today_currencies_rates_filename
#         else:
#             filename = filenames[0]
#         return cls.ROOT / filename

#     # @classproperty
#     # def today_currencies_rates_filename(cls):
#     #     return f"ecb_{date.today():%Y%m%d}.zip"

#     # @classproperty
#     # def certificate(cls):  # TODO : Add certificates
#     #     return cls.ROOT / "keys" / "other-csr.pem"
#     #     path_exists, path_created = cls.pathExists(filename="other-csr.pem")
#     #     if path_exists:
#     #         return path_created
#     #     else:
#     #         path_exists, path_created = cls.pathExists(filename="server-csr.pem")
#     #         return cls.formPathUsing(cls.PathInformation)

#     # @classproperty
#     # def privateKey(cls):  # TODO : Add keys
#     #     list_folders = ["", "keys"]
#     #     path_exists, path_created = cls.pathExists(
#     #         list_folders, "other-private-key.pem"
#     #     )
#     #     if path_exists:
#     #         return path_created
#     #     else:
#     #         path_exists, path_created = cls.pathExists(
#     #             list_folders, "server-private-key.pem"
#     #         )
#     #         return path_created


# class LogPath:
#     """Path to the logs of the application"""

#     ROOT = ROOT_PATH / Folder.LOGS.value

#     @classproperty
#     def application(cls):
#         return cls.ROOT / "application.log"

#     @classproperty
#     def db_com(cls):
#         return cls.ROOT / "db_com.log"

#     @classproperty
#     def error(cls):
#         return cls.ROOT / "error.log"

#     @classproperty
#     def logs_path(cls):
#         paths = [
#             getattr(LogPath, name)
#             for name in cls.__dict__.keys()
#             if not name.startswith("_") and name != "ROOT" and name != "logs_path"
#         ]
#         return paths


# class UserFilesPath:
#     """Path to the excels used :
#         -source excel (from the user (saved / imported) or from the folder examples)
#         -copy excel (copy of the source excel, cleaned and
#                     manipulated by the application, then removed)
#         If reaching USERS' file, 'ROOT' should be the excel's user folder"""

#     ROOT = APP_PATH / Folder.EXAMPLE.value

#     def __init__(self, username: str = None):
#         if username is not None:
#             self.username = username
#             self.ROOT = self.user_folder

#     @property
#     def user_folder(self):
#         return ROOT_PATH / Folder.DATA.value / Folder.USERS.value / self.username

#     @property
#     def excel(self):
#         return self.ROOT / "expenses.xlsx"

#     @property
#     def categories(self):
#         return self.ROOT / "categories.json"

#     @property
#     def translations(self):
#         return self.ROOT / "user_translations.json"

#     @classproperty
#     def example_excel(cls):
#         return cls.ROOT / "example_expenses_en.xlsx"

#     @classproperty
#     def example_short_excel(cls):
#         return cls.ROOT / "example_short_expenses_en.xlsx"

#     @classproperty
#     def example_categories(cls):
#         return cls.ROOT / "example_categories.json"

#     @classproperty
#     def example_translations(cls):
#         return cls.ROOT / "example_translations.json"


# #     def getNotebookConfigPath(self):
# #         self.PathInformation.folders = [self.notebook_excel]
# #         self.PathInformation.filename = "categories_themes_authorized_test.json"
# #         return self.formPathUsing(self.PathInformation)


# # @property
# #     def getStandardButtonsConfigPath(self):
# #         self.PathInformation.folders = [self.vues_folder, self.standard_buttons]
# #         self.PathInformation.filename = "config_buttons.json"
# #         return self.formPathUsing(self.PathInformation)


# class UnittestFilesPath:
#     """Path to the files used by the unittests"""

#     ROOT = APP_PATH / Folder.TEST.value / "test_files"

#     @classproperty
#     def folder(cls):
#         return cls.ROOT

#     @classproperty
#     def pipeline_test_values(cls):
#         """Returns the paired input output files for the tests of pipeline"""
#         input_files = [
#             path
#             for path in cls.ROOT.iterdir()
#             if path.is_file() and ("excel_input" in path.stem)
#         ]
#         output_files = [
#             path
#             for path in cls.ROOT.iterdir()
#             if path.is_file() and ("pipeline_output" in path.stem)
#         ]

#         paired_test_files = []
#         for input_file in input_files:
#             filename = input_file.stem
#             number = filename.split("_")[-1]

#             output_file = next(
#                 output_file
#                 for output_file in output_files
#                 if number in output_file.stem
#             )
#             paired_test_files.append([input_file, output_file])
#         return paired_test_files

#     # TODO
#     @classproperty
#     def convert_df_to_sql_test_values(cls):
#         """Returns the paired input output files for the tests of convert"""
#         input_files = [
#             path
#             for path in cls.ROOT.iterdir()
#             if path.is_file() and ("excel_input" in path.stem)
#         ]
#         output_files = [
#             path
#             for path in cls.ROOT.iterdir()
#             if path.is_file() and ("convert_df_to_sql_output" in path.stem)
#         ]

#         paired_test_files = []
#         for input_file in input_files:
#             filename = input_file.stem
#             number = filename.split("_")[-1]

#             output_file = next(
#                 output_file
#                 for output_file in output_files
#                 if number in output_file.stem
#             )
#             paired_test_files.append([input_file, output_file])
#         return paired_test_files

#     @classmethod
#     def getInputFileNumber(cls, number):
#         return next(
#             [
#                 path
#                 for path in cls.ROOT.iterdir()
#                 if path.is_file()
#                 and ("excel_input" in path.stem)
#                 and (number in path.stem)
#             ]
#         )

#     @classmethod
#     def getOutputFileNumber(cls, number):
#         return next(
#             [
#                 path
#                 for path in cls.ROOT.iterdir()
#                 if path.is_file()
#                 and ("pipeline_output" in path.stem)
#                 and (number in path.stem)
#             ]
#         )

