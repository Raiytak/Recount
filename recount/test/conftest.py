import typing
import pytest

from database.sql_db import Table, UserSqlTable
from file_management import FileAccessor, TestManager, UserManager

from excel_manager import ExcelManager
from database_manager import DatabaseManager

from pipeline.pipeline import cleanDf


@pytest.fixture
def username():
    return "hello"


@pytest.fixture
def table_name():
    return Table.EXPENSE


@pytest.fixture
def user_manager(username) -> typing.Type[UserManager]:
    user_manager = UserManager(username)
    return user_manager


@pytest.fixture
def excel_manager(user_manager) -> typing.Type[ExcelManager]:
    return ExcelManager(user_manager)


@pytest.fixture
def user_table(username, table_name) -> typing.Type[UserSqlTable]:
    user_table = UserSqlTable(username, table_name)
    yield user_table
    user_table.truncateUserOfTable()


@pytest.fixture
def database_manager(user_table) -> typing.Type[DatabaseManager]:
    return DatabaseManager(user_table)


@pytest.fixture
def excel_1():
    return TestManager.EXCEL_1


@pytest.fixture
def df_input_1(excel_manager, excel_1):
    df = excel_manager.dataframe(filepath=excel_1)
    return df


@pytest.fixture
def cleaned_df_input_1(df_input_1):
    cleaned_df = cleanDf(df_input_1, False)
    return cleaned_df


@pytest.fixture
def json_df_output_1():
    data_json = FileAccessor.readJson(filepath=TestManager.OUTPUT_JSON_1)
    return data_json


@pytest.fixture
def use_excel_1_in_db(cleaned_df_input_1, database_manager: DatabaseManager):
    database_manager.saveDataframe(cleaned_df_input_1)
