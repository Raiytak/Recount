import datetime
import pandas as pd
import json

from .conftest import *


def test_sql_database(user_table):
    assert user_table.columns_name == EXPECTED_DEFAULT_COLUMNS_NAME


EXPECTED_RESPONSE = {
    "id": {"0": 1},
    "username": {"0": "hello"},
    "date": {"0": 1577836800000},
    "amount": {"0": 10.0},
    "currency": {"0": "EUR"},
    "category": {"0": None},
    "receiver": {"0": None},
    "place": {"0": None},
    "description": {"0": None},
    "payment_method": {"0": "card"},
}


def test_sql_insertion(user_table):

    sql_request = SqlRequest(
        SqlKeyword.INSERT,
        Table.EXPENSE,
        username="hello",
        insert_columns=("id", "date", "amount", "currency"),
        insert_values=(1, datetime.datetime(2020, 1, 1), 10, "EUR"),
    )
    user_table.insert(sql_request)
    sql_request = SqlRequest(SqlKeyword.SELECT, Table.EXPENSE, "*")
    df = user_table.select(sql_request)
    data_json_str = df.to_json()
    data_json = json.loads(data_json_str)
    assert data_json == EXPECTED_RESPONSE
