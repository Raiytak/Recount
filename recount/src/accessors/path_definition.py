# -*- coding: utf-8 -*-
"""
Paths of the files used in the app
"""

from pathlib import Path

__all__ = ["RootFolder", "DataFolder", "LogFolder", "KeyFolder"]


class RecountSrcRoot:
    ROOT = Path(__file__).parent.parent.parent
    TEST = ROOT / "test"


class RootFolder:
    HOME = Path.home()
    ROOT = HOME / ".recount"

    ASSET = ROOT / "asset"
    CONFIG = ROOT / "config"
    DATA = ROOT / "data"
    KEY = ROOT / "key"
    LOGIN = ROOT / "login"
    LOG = ROOT / "log"


class AssetFolder:
    ROOT = RootFolder.ASSET
    DEFAULT = Path(__file__).parent.parent.parent.parent / "asset"


class KeyFolder:
    ROOT = RootFolder.KEY

    _DEFAULT_EXCEL_KEY_NAME = "default_excel.key"


class ConfigFolder:
    ROOT = RootFolder.CONFIG

    SQL_PATH = ROOT / "sql.config"


class LoginFolder:
    ROOT = RootFolder.LOGIN

    LOGIN_FILE = ROOT / "login.json"


class LogFolder:
    ROOT = RootFolder.LOG
    APP = ROOT / "app.log"
    APP_ERROR = ROOT / "app_error.log"
    SQL = ROOT / "sql_communcation.log"


class DataFolder:
    ROOT = RootFolder.DATA


class UsersFolder:
    ROOT = DataFolder.ROOT / "user"

    DEFAULT_EXCEL_NAME = "default.xlsx"


class ExampleFolder:
    ROOT = RecountSrcRoot.ROOT / "example"

    SQL_CONFIG = ROOT / "example_sql_config.json"
    EXCEL_PATH = ROOT / "example_expenses_en.xlsx"
    LOGIN = ROOT / "example_login.json"


class TestFolder:
    ROOT = RecountSrcRoot.TEST
    FILES = ROOT / "test_files"

    EXCEL_1 = FILES / "excel_input_1.xlsx"
    OUTPUT_JSON_1 = FILES / "dataframe_output_1.json"
    OUTPUT_PIPELINE_JSON_1 = FILES / "pipeline_output_1.json"
    DATABASE_DATAFRAME_JSON_1 = FILES / "database_dataframe_1.json"
    DATABASE_SAVE_DATAFRAME_1 = FILES / "database_save_dataframe_1.binary"
