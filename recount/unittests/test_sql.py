from .__init__ import *

from unittest.mock import Mock
import pytest
from threading import Thread
from time import sleep, perf_counter
from unittest.mock import patch

from com.sql import (
    Table,
    SqlManagerSingleton,
    SqlSocketManager,
    SqlKeyword,
    SqlRequest,
    SqlTable,
    UserSqlTable,
)

# TODO:
#   - assert all functions work
#   - assert list requests work


def test_sql_manager_singleton():
    assert SqlManagerSingleton.instance_alread_exists(DB_CONFIG) == False
    assert sum(1 for x in SqlManagerSingleton.instances) == 0
    manager_a = SqlManagerSingleton(DB_CONFIG)
    manager_b = SqlManagerSingleton(DB_CONFIG)
    assert manager_a == manager_b
    assert manager_a.db_config == DB_CONFIG
    assert sum(1 for x in manager_a.instances) == 1

    db_config_b = "hi"
    manager_c = SqlManagerSingleton(db_config_b)
    assert manager_a != manager_c
    assert sum(1 for x in manager_a.instances) == 2

    assert SqlManagerSingleton.instance_alread_exists(DB_CONFIG)
    assert SqlManagerSingleton.get_instance_named(DB_CONFIG) == manager_a
    assert SqlManagerSingleton.get_instance_named(db_config_b) == manager_c


@patch("com.sql.SqlSocket")
def test_sql_socket_manager(mocked_sql_socket):
    NUMBER_THREADS = 10
    SLEEP_TIME = 0.01

    def performFakeSqlRequests(socket_manager, sleep_time):
        with socket_manager:
            sleep(sleep_time)

    socket_managers = [SqlSocketManager(DB_CONFIG) for i in range(NUMBER_THREADS)]
    # Create two new threads
    threads = [
        Thread(
            target=performFakeSqlRequests,
            kwargs={"socket_manager": manager, "sleep_time": SLEEP_TIME},
        )
        for manager in socket_managers
    ]

    start_time = perf_counter()
    # Start the threads
    for thread in threads:
        thread.start()
    # Wait for the threads to complete
    for thread in threads:
        thread.join()

    end_time = perf_counter()
    time_delta = end_time - start_time
    sleep_delta = NUMBER_THREADS * SLEEP_TIME

    assert (time_delta > sleep_delta) and (time_delta <= sleep_delta + 0.1)


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
        f"UPDATE expense SET value='{update_value}' WHERE id='1';",
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

