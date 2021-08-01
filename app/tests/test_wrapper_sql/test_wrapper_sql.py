import pytest
import re
import enum

from wrapper_sql import wrapper_sql


CONFIG_ONE = {
    "mysql": {
        "host": "localhost",
        "port": 3306,
        "db": "expenses",
        "user": "myuser",
        "passwd": "mypass",
    }
}

CONFIG_TWO = {
    "mysql": {
        "host": "db",
        "port": 33000,
        "db": "expenses",
        "user": "myuser",
        "passwd": "mypass",
    }
}


def test_sql_connector(mocker):
    mocker.patch("pymysql.connect")
    spy_connection = mocker.spy(wrapper_sql.pymysql, "connect")

    sqlConnector = wrapper_sql.SQLConnector(CONFIG_ONE)
    assert spy_connection.call_count == 1
    assert sqlConnector.config["host"] == "localhost"

    sqlConnector.connect(CONFIG_TWO)
    assert spy_connection.call_count == 2
    assert sqlConnector.config["port"] == 33000


def test_execute(mocker):
    mocker.patch("pymysql.connect")
    spy_connection = mocker.spy(wrapper_sql.pymysql, "connect")
    fakeWrapper = wrapper_sql.WrapperOfTable("fake_table", CONFIG_ONE)
    spy_execution = mocker.spy(wrapper_sql.WrapperOfTable, "_execute")

    assert spy_connection.call_count == 1
    assert fakeWrapper.table == "fake_table"

    fake_request = "SELECT * FROM & WHERE ID = 0"
    response = fakeWrapper._execute(fake_request)

    assert spy_execution.call_count == 1


def test_select(mocker):
    mocker.patch("pymysql.connect")
    spy_connection = mocker.spy(wrapper_sql.pymysql, "connect")
    fakeWrapper = wrapper_sql.WrapperOfTable("fake_table", CONFIG_ONE)
    spy_response = mocker.spy(fakeWrapper.cursor, "fetchall")

    fake_request = "SELECT * FROM & WHERE ID = 0"
    response = fakeWrapper.select(fake_request)

    assert spy_connection.call_count == 1
    assert spy_response.call_count == 1


def test_insertion(mocker):
    mocker.patch("pymysql.connect")
    fakeWrapper = wrapper_sql.WrapperOfTable("fake_table", CONFIG_ONE)
    spy_commit = mocker.spy(fakeWrapper.myConnection, "commit")
    spy_response = mocker.spy(fakeWrapper.cursor, "fetchall")

    fake_request = "SELECT * FROM & WHERE ID = 0"
    response = fakeWrapper.insert(fake_request)

    assert spy_commit.call_count == 1
    assert spy_response.call_count == 1
    assert spy_response.spy_return != ()

    # mocker.patch(fakeWrapper.cursor, "fetchall", ())
    # with pytest.raises(
    #     ValueError,
    #     match=re.escape(f"SQL insertion error : ")
    # ):
    #     response = fakeWrapper.insert(fake_request)
