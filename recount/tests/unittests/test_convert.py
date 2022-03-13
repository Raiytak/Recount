from .__init__ import *

import pytest
import json

from src.access.access_files import UnittestFilesAccess
import src.pipeline.convert as convert


@pytest.mark.parametrize(
    ("df", "expected"), UnittestFilesAccess.convert_df_to_sql_test_values
)
def test_translate_df_to_sql_requests(df, expected):
    USER_DATA_PIPELINE.cleanDataframe(df)
    requests = convert.translateDataframeIntoInsertRequests(df, USER_TABLE)
    for request, exp in zip(requests, expected):
        assert str(request) == exp
    # Use to update the test file
    # with open(expected, "w") as file:
    #     text = "\n".join([str(req) for req in requests])
    #     file.write(text)


# TODO: Add magic mock in __init__ file to mock sql
@pytest.mark.parametrize(
    ("start_date", "end_date", "expected"),
    [
        [
            "2019-09-02",
            "2019-09-03",
            {
                "ID": {"0": 60, "1": 61},
                "username": {"0": "hello", "1": "hello"},
                "date": {"0": 1567468800000, "1": 1567468800000},
                "amount": {"0": 7.0, "1": 57.57},
                "category": {"0": "leasure:pub", "1": "alimentary:food"},
                "travel": {"0": None, "1": None},
                "company": {"0": "pub universitaire", "1": "metro"},
                "description": {"0": "soiree", "1": "nourriture"},
                "payment_method": {"0": "card", "1": "card"},
            },
        ],
        [
            "2019-09-02",
            "2019-09-02",
            {
                "ID": {},
                "username": {},
                "date": {},
                "amount": {},
                "category": {},
                "travel": {},
                "company": {},
                "description": {},
                "payment_method": {},
            },
        ],
    ],
)
def test_convert_date_to_df(start_date, end_date, expected):
    df = convert.convertDateToDataframe(start_date, end_date, USER_TABLE)
    df_json = df.to_json()
    cleaned_json = json.loads(df_json)
    assert cleaned_json == expected


@pytest.mark.parametrize(("start_date", "end_date",), [["2019-09-02", "2019-09-05"]])
def test_convert_df_to_expense_uniq_value_in_column(start_date, end_date):
    df = convert.convertDateToDataframe(start_date, end_date, USER_TABLE)
    response = convertDataframeToGraphDataForEachUniqValueInColumn(df, "category")
    expected_keys = {"x", "y", "text", "name"}
    response_col = response[0]
    assert response_col.keys() >= expected_keys
    assert all(
        [
            len(value) == len(response_col["x"])
            for key, value in response_col.items()
            if key != "name"
        ]
    )


@pytest.mark.parametrize(("start_date", "end_date",), [["2019-09-02", "2019-09-05"]])
def test_convert_df_to_expense_uniq_value_in_column(start_date, end_date):
    df = convert.convertDateToDataframe(start_date, end_date, USER_TABLE)
    response = convertDataframeToSumDataForEachUniqValueInColumn(df, "category")
    expected_keys = {"values", "names", "labels"}
    response_col = response[0]
    assert response_col.keys() >= expected_keys
    assert all(
        [len(value) == len(response_col["values"]) for value in response_col.values()]
    )
