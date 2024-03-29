""" 
Creation and management MySQL connections and requests.
"""


import logging
import pandas as pd
from enum import Enum
from collections import namedtuple
from typing import Union, List
import pymysql

from accessors.file_management import ConfigManager

__all__ = ["DbConf", "Table", "SqlKeyword", "SqlRequest", "SqlTable", "UserSqlTable"]


class Table(Enum):
    """Name of the available tables"""

    EXPENSE = "expense"  # Default table
    # REIMBURSEMENT = "reimbursement"
    INFORMATION_COLUMNS = "information_schema.columns"


class DbConf(Enum):
    HOST = "localhost"
    PORT = 3306
    DB = "recount"
    USER = "localhost"
    PASSWORD = None
    SSL = None


class SqlSocket:
    """Create and manage a connection to the MySQL database"""

    def __init__(self, config: dict = None, table: Table = Table.EXPENSE):
        # TODO: use table
        if config is None:
            json_config = ConfigManager.sqlConfig()
            # Get default values for those unset
            for item in DbConf:
                key = item.name.lower()
                if not key in json_config.keys():
                    json_config[key] = item.value
            config = json_config
        self.connection, self.cursor = self.createSocket(config)

    def createSocket(self, config: dict, enable_ssl: bool = True):
        if enable_ssl:
            config["ssl"] = {"fake_flag_to_enable_tls": True}
        new_socket = pymysql.connect(
            host=config["host"],
            user=config["user"],
            passwd=config["password"],
            port=config["port"],
            db=config["db"],
            ssl=config["ssl"],
        )
        return new_socket, new_socket.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        del self


class SqlKeyword(Enum):
    SELECT = "SELECT"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
    INSERT = "INSERT INTO"
    TRUNCATE = "TRUNCATE TABLE"

    FROM = "FROM"
    WHERE = "WHERE"
    ORDER = "ORDER BY"
    GROUP = "GROUP BY"
    SET = "SET"
    LIMIT = "LIMIT"
    VALUES = "VALUES"


class SqlRequest:
    INTERNAL_VARIABLES = [
        "action",
        "table_name",
        "column",
        "condition",
        "username",
        "group",
        "order",
        "limit",
        "change",
        "insert_columns",
        "insert_values",
        "by_hand",
    ]

    def __init__(
        self,
        action: SqlKeyword,
        table: Table = None,
        column: Union[str, List[str]] = None,  # TODO: make the case list
        condition: str = None,
        username: str = None,
        group: str = None,
        order: str = None,
        limit: str = None,
        change: str = None,
        insert_dict_values: dict = None,
        insert_columns: Union[tuple, list] = (),
        insert_values: Union[tuple, list] = (),
        by_hand: str = None,
    ) -> None:
        """
        :arg by_hand: useful to specify by hand the request, except for 'action' and 'table'
        """
        # Assert that data provided can be accepted
        if insert_dict_values:
            if insert_columns or insert_values:
                raise AttributeError(
                    "'insert_dict_values' can't be used at the same time as 'insert_columns' and 'insert_values'"
                )
            insert_columns = [key for key in insert_dict_values.keys()]
            insert_values = [value for value in insert_dict_values.values()]
        if len(insert_columns) != len(insert_values):
            raise AttributeError(
                "'insert_columns' and 'insert_values' have different length"
            )

        self.action = action.value if type(action) is SqlKeyword else action
        if action == SqlKeyword.INSERT:
            self.table_name = table.value
        else:
            self.table_name = (
                table
                if (action == SqlKeyword.UPDATE) or (table is None)
                else self.concatenateIfValueNotNone(
                    table.value, SqlKeyword.FROM.value + " "
                )
            )
        self.column = (
            self.concatenateOrNone(*column, joint=", ")
            if type(column) == list
            else column
        )
        self.condition = self.concatenateIfValueNotNone(
            self.concatenateConditionAndUsername(condition, username),
            SqlKeyword.WHERE.value + " ",
        )
        self.username = username
        self.order = self.concatenateIfValueNotNone(order, SqlKeyword.ORDER.value + " ")
        self.group = self.concatenateIfValueNotNone(group, SqlKeyword.GROUP.value + " ")
        self.change = self.concatenateIfValueNotNone(change, SqlKeyword.SET.value + " ")
        self.limit = self.concatenateIfValueNotNone(limit, SqlKeyword.LIMIT.value + " ")
        self.insert_columns = insert_columns
        self.insert_values = insert_values
        self.by_hand = by_hand

    def __str__(self) -> str:
        if self.action == SqlKeyword.SELECT.value:
            return self.createSelectRequest()
        elif self.action == SqlKeyword.UPDATE.value:
            return self.createUpdateRequest()
        elif self.action == SqlKeyword.INSERT.value:
            return self.createInsertRequest()
        elif self.action == SqlKeyword.DELETE.value:
            return self.createDeleteRequest()
        elif self.action == SqlKeyword.TRUNCATE.value:
            return self.createTruncateRequest()
        raise Exception

    @property
    def values(self) -> str:
        return ", ".join(
            [var + ": " + str(getattr(self, var)) for var in self.INTERNAL_VARIABLES]
        )

    @staticmethod
    def concatenate(*args, joint=" ", end=""):
        existing_args = filter(lambda arg: not arg is None, args)
        request = joint.join(existing_args)
        return request + end

    @staticmethod
    def concatenateIfValueNotNone(value, pre_value=None, after_value=None, joint=""):
        if value:
            return SqlRequest.concatenate(pre_value, value, after_value, joint=joint)
        return None

    @staticmethod
    def concatenateOrNone(*args, joint=" "):
        if all(arg is None for arg in args):
            return None
        return SqlRequest.concatenate(*args, joint=joint)

    @staticmethod
    def concatenateConditionAndUsername(condition, username):
        username = SqlRequest.concatenateIfValueNotNone(username, "username='", "'")
        return SqlRequest.concatenateOrNone(condition, username, joint=" AND ")

    def prepareInsertRequest(self):
        if not self.username:
            raise AttributeError("username not provided for an insert request")
        cleaned_insert_values = (
            [
                "'" + str(value) + "'"
                for value in self.insert_values
                if not (pd.isnull(value) or value == "nan")
            ]
            if not self.insert_values is None
            else self.insert_values
        )
        cleaned_insert_values.append("'" + self.username + "'")

        cleaned_insert_columns = (
            [
                column
                for (column, value) in zip(self.insert_columns, self.insert_values)
                if not (pd.isnull(value) or value == "nan")
            ]
            if not self.insert_columns is None
            else self.insert_columns
        )
        cleaned_insert_columns.append("username")

        self.cleaned_insert_columns = self.concatenateIfValueNotNone(
            self.concatenateOrNone(*cleaned_insert_columns, joint=", "), "(", ")"
        )
        self.cleaned_insert_values = self.concatenateIfValueNotNone(
            self.concatenateOrNone(*cleaned_insert_values, joint=", "),
            f"{SqlKeyword.VALUES.value} (",
            ")",
        )

    def createSelectRequest(self):
        request = self.concatenate(
            self.action,
            self.column,
            self.table_name,
            self.condition,
            self.group,
            self.order,
            self.limit,
            self.by_hand,
            end=";",
        )
        return request

    def createUpdateRequest(self):
        request = self.concatenate(
            self.action,
            self.table_name,
            self.change,
            self.condition,
            self.order,
            self.limit,
            self.by_hand,
            end=";",
        )
        return request

    def createDeleteRequest(self):
        request = self.concatenate(
            self.action, self.table_name, self.condition, self.by_hand, end=";"
        )
        return request

    def createInsertRequest(self):
        self.prepareInsertRequest()
        request = self.concatenate(
            self.action,
            self.table_name,
            self.cleaned_insert_columns,
            self.cleaned_insert_values,
            self.by_hand,
            end=";",
        )
        return request

    def createTruncateRequest(self):
        request = self.concatenate(
            self.action,
            self.table_name,
            end=";",
        )
        return request


class SqlTable:
    """Access to one table of the"""

    # TODO : assert table exists
    def __init__(self, table: Table = None, config: dict = None):
        if not table:
            table = Table.EXPENSE  # Default table
        self.table = table
        self.table_name = table.value
        self.config = config

    def _execute(self, sql_request: SqlRequest, sql_socket: SqlSocket):
        # The encryption is taking too long, commented for now
        # encrypted_insertion = self.SqlEncryption.encryptInsertion(sql_request)
        request = str(sql_request)
        response = sql_socket.cursor.execute(request)
        return response

    def _select(self, sql_request: SqlRequest) -> str:
        with SqlSocket(self.config) as sql_socket:
            self._execute(sql_request, sql_socket)
            return sql_socket.cursor.fetchall()

    def select(self, sql_request: SqlRequest):
        with SqlSocket(self.config) as sql_socket:
            request = str(sql_request)
            df = pd.read_sql(request, sql_socket.connection)
            return df

    def insert(self, sql_request: SqlRequest):
        with SqlSocket(self.config) as sql_socket:
            try:
                self._execute(sql_request, sql_socket)
                sql_socket.connection.commit()
            except Exception as exc:
                print(f"Exception during commit : '{exc}'")
                print(f"The request was the following:\n{sql_request}")
                logging.warning("Trying a rollback ... ")
                try:
                    sql_socket.connection.rollback()
                except Exception as exc2:
                    logging.warning("ROLLBACK FAILED!")
                    raise exc2
                logging.warning("Rollback done!")
                raise exc

            response = sql_socket.cursor.fetchall()
            if response != ():
                return ValueError(f"SQL insertion error : '{response}'")

    def delete(self, sql_request: SqlRequest):
        with SqlSocket(self.config) as sql_socket:
            self._execute(sql_request, sql_socket)

    @property
    def database_name(self) -> str:
        request = SqlRequest(action=SqlKeyword.SELECT, by_hand="DATABASE()")
        response = self._select(request)
        return response[0][0]

    @property
    def columns_name(self) -> list:
        request = SqlRequest(
            action=SqlKeyword.SELECT,
            column="column_name",
            table=Table.INFORMATION_COLUMNS,
            condition=f"table_schema='{self.database_name}' AND table_name='{self.table_name}'",
            order="table_name, ordinal_position",
        )
        response = self._select(request)
        name_columns = [col[0] for col in response]
        return name_columns

    def selectAll(self):
        request = SqlRequest(action=SqlKeyword.SELECT, column="*", table=self.table)
        return self.select(request)

    def truncateTable(self):
        request = SqlRequest(action=SqlKeyword.TRUNCATE, table=self.table)
        self.delete(request)


class UserSqlTable(SqlTable):
    def __init__(self, username: str, table: Table, config: dict = None):
        super().__init__(table, config)
        self.username = username

    def insert(self, sql_request: SqlRequest):
        sql_request.username = self.username
        return super().insert(sql_request)

    def select(self, sql_request: SqlRequest) -> pd.DataFrame:
        sql_request.username = self.username
        return super().select(sql_request)

    def selectAll(self):
        request = SqlRequest(
            action=SqlKeyword.SELECT,
            column="*",
            table=self.table,
            username=self.username,
        )
        return self.select(request)

    def delete(self, sql_request: SqlRequest):
        sql_request.username = self.username
        return super().delete(sql_request)

    def truncateUserOfTable(self):
        request = SqlRequest(
            action=SqlKeyword.DELETE, table=self.table, username=self.username
        )
        self.delete(request)

    def selectRowId(self, id):
        request = SqlRequest(
            action=SqlKeyword.SELECT,
            table=self.table,
            condition=f"ID = {str(id)}",
            username=self.username,
        )
        return self.select(request)
