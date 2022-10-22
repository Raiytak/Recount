from .defaults import *
from accessors.file_management import UserManager


USERNAME = "hello"
DB_CONFIG = {}
TABLE_NAME = Table.EXPENSE
EXPECTED_DEFAULT_COLUMNS_NAME = [
    "ID",
    "username",
    "date",
    "amount",
    "category",
    "travel",
    "company",
    "description",
    "payment_method",
]

USER_ACCESS = UserManager(USERNAME)
USER_TABLE = UserSqlTable(USERNAME, TABLE_NAME)


def test_sql_database():
    assert USER_TABLE.columns_name == EXPECTED_DEFAULT_COLUMNS_NAME
