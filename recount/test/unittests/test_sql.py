from .conftest import *

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
    "category",
    "travel",
    "company",
    "description",
    "payment_method",
]


def defaultSelectExpenseResponses(request):
    if (
        str(request)
        == "SELECT * FROM expense WHERE date >= '2019-09-02' AND date <= '2019-09-03' AND username='hello';"
    ):
        return (
            (
                60,
                "hello",
                datetime.date(2019, 9, 3),
                7.0,
                "leasure:pub",
                None,
                "pub universitaire",
                "soiree",
                "card",
            ),
            (
                61,
                "hello",
                datetime.date(2019, 9, 3),
                57.57,
                "alimentary:food",
                None,
                "metro",
                "nourriture",
                "card",
            ),
        )
    return ()


update_value = "hi"

# TODO: Improve
username = "hello"
table_name = Table.EXPENSE

NoException = None
requests_to_evaluate = [
    (
        (SqlKeyword.SELECT, table_name, "*", None, username),
        f"SELECT * FROM {table_name.value} WHERE username='{username}';",
        NoException,
    ),
    (
        (
            SqlKeyword.SELECT,
            table_name,
            ["column_a", "column_b", "column_c"],
            "value='expected'",
            username,
        ),
        f"SELECT column_a, column_b, column_c FROM {table_name.value} WHERE value='expected' AND username='{username}';",
        NoException,
    ),
    (
        (SqlKeyword.DELETE, table_name, None, None, username),
        f"DELETE FROM {table_name.value} WHERE username='{username}';",
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
        f"UPDATE {table_name.value} SET value='{update_value}' WHERE id='1';",
        NoException,
    ),
    (
        (
            SqlKeyword.SELECT,
            table_name,
            ["*"],
            "value='expected'",
            username,
            "username",
            "id",
            "5",
        ),
        f"SELECT * FROM {table_name.value} WHERE value='expected' AND username='{username}' GROUP BY username ORDER BY id LIMIT 5;",
        NoException,
    ),
    (
        (
            SqlKeyword.INSERT,
            table_name,
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
        f"INSERT INTO {table_name.value} (col 1, col 2, col 3) VALUES ('val 1', 'val 2', 'val 3');",
        NoException,
    ),
    (
        (
            SqlKeyword.INSERT,
            table_name,
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
        f"INSERT INTO {table_name.value} VALUES ('val 1', 'val 2', 'val 3');",
        AttributeError,
    ),
    (
        (
            SqlKeyword.INSERT,
            table_name,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {"col 1": "val 1", "col 2": "val 2", "col 3": "val 3"},
        ),
        f"INSERT INTO {table_name.value} (col 1, col 2, col 3) VALUES ('val 1', 'val 2', 'val 3');",
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
