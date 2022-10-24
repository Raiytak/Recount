import typing
import pytest

from file_management import FileAccessor, TestManager

from database_manager import DatabaseManager


@pytest.fixture
def database_manager(user_manager) -> typing.Type[DatabaseManager]:
    return DatabaseManager(user_manager)
