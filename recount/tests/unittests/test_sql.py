from .defaults import *

from database.sql_db import (
    Table,
    SqlKeyword,
    SqlRequest,
    SqlTable,
    UserSqlTable,
)


update_value = "hi"

NoException = None
requests_to_evaluate = [
    (
        (SqlKeyword.SELECT, TABLE_NAME, "*", None, USERNAME),
        f"SELECT * FROM {TABLE_NAME.value} WHERE username='{USERNAME}';",
        NoException,
    ),
    (
        (
            SqlKeyword.SELECT,
            TABLE_NAME,
            ["column_a", "column_b", "column_c"],
            "value='expected'",
            USERNAME,
        ),
        f"SELECT column_a, column_b, column_c FROM {TABLE_NAME.value} WHERE value='expected' AND username='{USERNAME}';",
        NoException,
    ),
    (
        (SqlKeyword.DELETE, TABLE_NAME, None, None, USERNAME),
        f"DELETE FROM {TABLE_NAME.value} WHERE username='{USERNAME}';",
        NoException,
    ),
    (
        (
            SqlKeyword.UPDATE,
            Table.EXPENSE.value,
            None,
            "id='1'",
            None,
            None,
            None,
            None,
            f"value='{update_value}'",
        ),
        f"UPDATE {TABLE_NAME.value} SET value='{update_value}' WHERE id='1';",
        NoException,
    ),
    (
        (
            SqlKeyword.SELECT,
            TABLE_NAME,
            ["*"],
            "value='expected'",
            USERNAME,
            "username",
            "id",
            "5",
        ),
        f"SELECT * FROM {TABLE_NAME.value} WHERE value='expected' AND username='{USERNAME}' GROUP BY username ORDER BY id LIMIT 5;",
        NoException,
    ),
    (
        (
            SqlKeyword.INSERT,
            TABLE_NAME,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            ["col 1", "col 2", "col 3"],
            ["val 1", "val 2", "val 3"],
        ),
        f"INSERT INTO {TABLE_NAME.value} (col 1, col 2, col 3) VALUES ('val 1', 'val 2', 'val 3');",
        NoException,
    ),
    (
        (
            SqlKeyword.INSERT,
            TABLE_NAME,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            (),
            ["val 1", "val 2", "val 3"],
        ),
        f"INSERT INTO {TABLE_NAME.value} VALUES ('val 1', 'val 2', 'val 3');",
        AttributeError,
    ),
    (
        (
            SqlKeyword.INSERT,
            TABLE_NAME,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"col 1": "val 1", "col 2": "val 2", "col 3": "val 3"},
        ),
        f"INSERT INTO {TABLE_NAME.value} (col 1, col 2, col 3) VALUES ('val 1', 'val 2', 'val 3');",
        NoException,
    ),
]


@pytest.mark.parametrize(
    argnames=("request_input", "expected_request", "expected_exception"),
    argvalues=requests_to_evaluate,
)
def test_sql_request(request_input, expected_request, expected_exception):
    try:
        assert str(SqlRequest(*request_input)) == expected_request
    except expected_exception:
        pass
