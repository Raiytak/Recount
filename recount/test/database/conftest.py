import pytest
from unittest.mock import MagicMock, patch

from database.sql_db import (
    Table,
    SqlKeyword,
    SqlRequest,
    SqlTable,
    UserSqlTable,
)


EXPECTED_DEFAULT_COLUMNS_NAME = [
    "ID",
    "username",
    "date",
    "amount",
    "currency",
    "category",
    "receiver",
    "place",
    "description",
    "payment_method",
]


@pytest.fixture
def username():
    return "hello"


@pytest.fixture
def table_name():
    return Table.EXPENSE


@pytest.fixture
def user_table(username, table_name):
    user_table = UserSqlTable(username, table_name)
    yield user_table
    user_table.truncateTableOfUser()


# def defaultSelectExpenseResponses(request):
#     if (
#         str(request)
#         == "SELECT * FROM expense WHERE date >= '2019-09-02' AND date <= '2019-09-03' AND username='hello';"
#     ):
#         return (
#             (
#                 60,
#                 "hello",
#                 datetime.date(2019, 9, 3),
#                 7.0,
#                 "leasure:pub",
#                 None,
#                 "pub universitaire",
#                 "soiree",
#                 "card",
#             ),
#             (
#                 61,
#                 "hello",
#                 datetime.date(2019, 9, 3),
#                 57.57,
#                 "alimentary:food",
#                 None,
#                 "metro",
#                 "nourriture",
#                 "card",
#             ),
#         )
#     return ()
