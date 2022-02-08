from unittest.mock import Mock
import pytest
import threading

from com.sql import (
    SqlSocket,
    SqlManagerSingleton,
    SqlSocketManager,
    SqlKeyword,
    SqlRequest,
    SqlTable,
    UserSqlTable,
)

# TODO:
#   - assert mutex works
#   - assert all functions work
#   - assert parallel request works (different instances but same connection)
#   - assert list requests work


def test_sql_manager_singleton():
    db_config = "hello"
    assert SqlManagerSingleton.instance_alread_exists(db_config) == False
    assert sum(1 for x in SqlManagerSingleton.instances) == 0
    manager_a = SqlManagerSingleton(db_config)
    manager_b = SqlManagerSingleton(db_config)
    assert manager_a == manager_b
    assert manager_a.db_config == db_config
    assert sum(1 for x in manager_a.instances) == 1

    db_config_b = "hi"
    manager_c = SqlManagerSingleton(db_config_b)
    assert manager_a != manager_c
    assert sum(1 for x in manager_a.instances) == 2

    assert SqlManagerSingleton.instance_alread_exists(db_config)
    assert SqlManagerSingleton.get_instance_named(db_config) == manager_a
    assert SqlManagerSingleton.get_instance_named(db_config_b) == manager_c


def test_sql_socket_manager():
    pass  # TODO


table_name = "my_table"
username = "hello"
update_value = "hi"


requests_to_evaluate = [
    (
        (SqlKeyword.SELECT, table_name, "*", None, username),
        f"SELECT * FROM {table_name} WHERE username='{username}';",
    ),
    (
        (
            SqlKeyword.SELECT,
            table_name,
            ["column_a", "column_b", "column_c"],
            "value='expected'",
            username,
        ),
        f"SELECT column_a, column_b, column_c FROM {table_name} WHERE value='expected' AND username='{username}';",
    ),
    (
        (SqlKeyword.DELETE, table_name, None, None, username),
        f"DELETE FROM {table_name} WHERE username='{username}';",
    ),
    (
        (
            SqlKeyword.UPDATE,
            table_name,
            None,
            "id='1'",
            None,
            None,
            None,
            None,
            f"value='{update_value}'",
        ),
        f"UPDATE {table_name} SET value='{update_value}' WHERE id='1';",
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
        f"SELECT * FROM {table_name} WHERE value='expected' AND username='{username}' GROUP BY username ORDER BY id LIMIT 5;",
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
            ["col 1", "col 2", "col 3"],
            ["val 1", "val 2", "val 3"],
        ),
        f"INSERT INTO {table_name} (col 1, col 2, col 3) VALUES ('val 1', 'val 2', 'val 3');",
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
            (),
            ["val 1", "val 2", "val 3"],
        ),
        f"INSERT INTO {table_name} VALUES ('val 1', 'val 2', 'val 3');",
    ),
]


@pytest.mark.parametrize(
    argnames=("request_input", "expected_request"), argvalues=requests_to_evaluate
)
def test_sql_request(request_input, expected_request):
    assert str(SqlRequest(*request_input)) == expected_request


# @pytest.fixture
# def sql_request():
#     request = Mock()
#     request.__str__ = f"SELECT * FROM {table_name}"
#     return request

# @pytest.fixture
# def socket():
#     cursor = Mock()
#     cursor.fetchall = lambda:True
#     cursor.execute = lambda:True

#     connection = Mock()
#     connection.commit = lambda:True
#     connection.rollback = lambda:True

#     socket = Mock()
#     socket.cursor = cursor
#     socket.connection = connection
#     return socket

# def sql_socket_manager():
#     manager = Mock()
#     manager.__enter__ = socket
#     manager.__exit__ = socket

# def test_sql_table():

