import datetime

from .conftest import *


def test_sql_database(user_table):
    assert user_table.columns_name == EXPECTED_DEFAULT_COLUMNS_NAME


def test_sql_insertion(user_table):

    sql_request = SqlRequest(
        SqlKeyword.INSERT,
        Table.EXPENSE,
        insert_columns=("ID", "username", "date", "amount", "currency"),
        insert_values=(1, "hello", datetime.datetime(2020, 1, 1), 10, "EUR"),
    )
    user_table.insert(sql_request)
    sql_request = SqlRequest(SqlKeyword.SELECT, Table.EXPENSE, "*")
    response = user_table.select(sql_request)
    assert response == (
        (
            1,
            "hello",
            datetime.date(2020, 1, 1),
            10.0,
            "EUR",
            None,
            None,
            None,
            None,
            "card",
        ),
    )
    user_table.truncateTableOfUser()
