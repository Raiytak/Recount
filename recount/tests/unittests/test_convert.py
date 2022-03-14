from .defaults import *

from access.access_files import UnittestFilesAccess
import pipeline.convert as convert


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


@pytest.mark.parametrize(
    ("start_date", "end_date", "expected"),
    [
        [
            "2019-09-02",
            "2019-09-03",
            {
                "username": {"60": "hello", "61": "hello"},
                "date": {"60": 1567468800000, "61": 1567468800000},
                "amount": {"60": 7.0, "61": 57.57},
                "category": {"60": "leasure:pub", "61": "alimentary:food"},
                "travel": {"60": None, "61": None},
                "company": {"60": "pub universitaire", "61": "metro"},
                "description": {"60": "soiree", "61": "nourriture"},
                "payment_method": {"60": "card", "61": "card"},
            },
        ],
    ],
)
def test_convert_date_to_df(start_date, end_date, expected):
    with patch("src.com.sql.UserSqlTable.select") as fake_select:
        fake_select.side_effect = defaultSelectExpenseResponses
        df = convert.convertDateToDataframe(start_date, end_date, USER_TABLE)
        df_json = df.to_json()
        cleaned_json = json.loads(df_json)
        assert cleaned_json == expected


@pytest.mark.parametrize(("start_date", "end_date",), [["2019-09-02", "2019-09-03"]])
def test_convert_df_to_expense_uniq_value_in_column(start_date, end_date):
    with patch("src.com.sql.UserSqlTable.select") as fake_select:
        fake_select.side_effect = defaultSelectExpenseResponses
        df = convert.convertDateToDataframe(start_date, end_date, USER_TABLE)
        response = convert.convertDataframeToGraphDataForEachUniqValueInColumn(
            df, "category"
        )
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


@pytest.mark.parametrize(("start_date", "end_date",), [["2019-09-02", "2019-09-03"]])
def test_convert_df_to_sum_expense_uniq_value_in_column(start_date, end_date):
    with patch("src.com.sql.UserSqlTable.select") as fake_select:
        fake_select.side_effect = defaultSelectExpenseResponses
        df = convert.convertDateToDataframe(start_date, end_date, USER_TABLE)
        response = convert.convertDataframeToSumDataForEachUniqValueInColumn(
            df, "category"
        )
        expected_keys = {"values", "names", "labels"}
        response_col = response
        assert response_col.keys() >= expected_keys
        assert all(
            [
                len(value) == len(response_col["values"])
                for value in response_col.values()
            ]
        )
