import typing
import pytest

from excel_interface import UserExcelManager
from accessors import file_management
from database.sql_db import Table


@pytest.fixture
def username():
    return "hello"


@pytest.fixture
def table_name():
    return Table.EXPENSE


@pytest.fixture
def mock_user_excel(username) -> typing.Type[UserExcelManager]:
    mock_user_excel = UserExcelManager(username)
    yield mock_user_excel
    del mock_user_excel


@pytest.fixture
def df_input(mock_user_excel):
    df = mock_user_excel.dataframe(filepath=file_management.TestManager.excel_1)
    return df


@pytest.fixture
def json_output(mock_user_excel):
    df = mock_user_excel.dataframe(filepath=file_management.TestManager.excel_1)
    return df


@pytest.fixture
def excel_manager(username):
    return UserExcelManager(username)
