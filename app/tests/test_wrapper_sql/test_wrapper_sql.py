import pytest
import enum

from wrapper_sql import wrapper_sql


CONFIG_ONE={
    "mysql": {
        "host": "localhost",
        "port": 3306,
        "db": "expenses",
        "user": "myuser",
        "passwd": "mypass"
    }
}

CONFIG_TWO={
    "mysql": {
        "host": "db",
        "port": 33000,
        "db": "expenses",
        "user": "myuser",
        "passwd": "mypass"
    }
}

class FakeConnection:
    def cursor(self):
        return ""

def test_connection(mocker):
    mocker.patch("pymysql.connect", return_value=FakeConnection())
    spy_connection = mocker.spy(wrapper_sql.pymysql, "connect")
   
    sqlConnector = wrapper_sql.SQLConnector(CONFIG_ONE)
    assert spy_connection.call_count == 1
    assert sqlConnector.config["host"] == "localhost"
   
    sqlConnector.connect(CONFIG_TWO)
    assert spy_connection.call_count == 2
    assert sqlConnector.config["port"] == 33000

