# -*- coding: utf-8 -*-

import typing
import pytest
import json

from excel_manager import ExcelManager
from accessors import file_management
from database.sql_db import Table
from file_management import FileAccessor, UserManager


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
    return file_management.TestManager.EXCEL_1


@pytest.fixture
def df_input_1(excel_manager, excel_1):
    df = excel_manager.dataframe(filepath=excel_1)
    return df


@pytest.fixture
def output_json_1():
    return file_management.TestManager.PATH_DF_OUTPUT_JSON_1


@pytest.fixture
def output_pipeline_json_1():
    return file_management.TestManager.PATH_DF_OUTPUT_PIPELINE_JSON_1


@pytest.fixture
def json_df_output_1(output_json_1):
    data_json = FileAccessor.readJson(filepath=output_json_1)
    return data_json


@pytest.fixture
def json_pipeline_output_1(output_pipeline_json_1):
    data_json = FileAccessor.readJson(filepath=output_pipeline_json_1)
    return data_json
