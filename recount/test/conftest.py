# -*- coding: utf-8 -*-

import typing
import pytest
import json

from excel_manager import ExcelManager
from accessors import file_management
from database.sql_db import Table
from src.accessors.file_management import FileAccessor, UserManager


@pytest.fixture
def username():
    return "hello"


@pytest.fixture
def table_name():
    return Table.EXPENSE


@pytest.fixture
def user_manager(username):
    user_manager = UserManager(username)
    return user_manager


@pytest.fixture
def excel_manager(user_manager) -> typing.Type[ExcelManager]:
    return ExcelManager(user_manager)


@pytest.fixture
def excel_1():
    return file_management.TestManager.excel_1


@pytest.fixture
def df_input_1(excel_manager, excel_1):
    df = excel_manager.dataframe(filepath=excel_1)
    return df


@pytest.fixture
def path_df_output_json_1():
    return file_management.TestManager.path_df_output_json_1


@pytest.fixture
def json_df_output_json_1(path_df_output_json_1):
    data_json = FileAccessor.readJson(filepath=path_df_output_json_1)
    return data_json
