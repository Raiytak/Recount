# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Creation and management of the MySQL connections, requests and return the responses.
"""

import logging
import pandas as pd
from enum import Enum
from typing import Union, List
import pymysql

from accessors.file_management import Config

__all__ = ["SqlRequest", "SqlTable", "UserSqlTable"]


class Table(Enum):
    """Name of the available tables"""

    EXPENSE = "expenses"  # Default table
    # REIMBURSEMENT = "reimbursement"
    INFORMATION_COLUMNS = "information_schema.columns"


class SqlSocket:
    """Create and manage a connection to the MySQL database"""

    def __init__(self, config=None):
        if config is None:
            config = Config.sql()  # Get the default config
        self.connection, self.cursor = self.createSocket(config)

    def createSocket(self, config, enable_ssl=True):
        config_ssl = None
        if enable_ssl:
            config_ssl = {"fake_flag_to_enable_tls": True}
        new_socket = pymysql.connect(
            host=config["host"],
            user=config["user"],
            passwd=config["password"],
            port=config["port"],
            db=config["db"],
            ssl=config_ssl,
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
        if len(insert_columns) != len(insert_values):
            raise AttributeError(
                "'insert_columns' and 'insert_values' have different length"
            )
        if insert_dict_values:
            if insert_columns or insert_values:
                raise AttributeError(
                    "'insert_dict_values' can't be used with 'insert_columns' or 'insert_values'"
                )
            insert_columns = [key for key in insert_dict_values.keys()]
            insert_values = [value for value in insert_dict_values.values()]

        cleaned_insert_values = (
            [
                "'" + str(value) + "'"
                for value in insert_values
                if not (pd.isnull(value) or value == "nan")
            ]
            if not insert_values is None
            else insert_values
        )

        cleaned_insert_columns = (
            [
                column
                for (column, value) in zip(insert_columns, insert_values)
                if not (pd.isnull(value) or value == "nan")
            ]
            if not insert_columns is None
            else insert_columns
        )

        assert len(cleaned_insert_columns) == len(cleaned_insert_values)
        self.insert_columns = self.concatenateIfValueNotNone(
            self.concatenateOrNone(*cleaned_insert_columns, joint=", "), "(", ")"
        )
        self.insert_values = self.concatenateIfValueNotNone(
            self.concatenateOrNone(*cleaned_insert_values, joint=", "),
            f"{SqlKeyword.VALUES.value} (",
            ")",
        )
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

    @staticmethod
    def concatenate(*args, joint=" ", end=""):
        useful_args = filter(lambda arg: not arg is None, args)
        request = joint.join(useful_args)
        return request + end

    @staticmethod
    def concatenateIfValueNotNone(value, pre_value=None, after_value=None, joint=""):
        if not value is None:
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
        request = self.concatenate(
            self.action,
            self.table_name,
            self.insert_columns,
            self.insert_values,
            self.by_hand,
            end=";",
        )
        return request

    def createTruncateRequest(self):
        request = self.concatenate(self.action, self.table_name, end=";",)
        return request


class SqlTable:
    """Access to one table of the """

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

    def select(self, sql_request: SqlRequest):
        with SqlSocket(self.config) as sql_socket:
            self._execute(sql_request, sql_socket)
            return sql_socket.cursor.fetchall()

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
        response = self.select(request)
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
        response = self.select(request)
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

    def selectAll(self):
        request = SqlRequest(
            action=SqlKeyword.SELECT,
            column="*",
            table=self.table,
            username=self.username,
        )
        return self.select(request)

    def truncateTableOfUser(self):
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

    def insertAllReqs(self, list_request_sql):
        for req_sql in list_request_sql:
            try:
                self.insert(req_sql)
            except pymysql.err.IntegrityError:
                pass
                # TODO: if ID exists, update / remove then insert
                # self.update


# import re


# class SqlEncryption:
#     """Encryption logic of the SQL exchanges."""

#     def __init__(self):
#         self.Config = Config()
#         sql_key = self.Config.getDataSqlKey()
#         self.list_columns_to_left_unchanged = [
#             "ID",
#             "_id",
#             "date",
#             "username",
#             "payment_method",
#         ]
#         super().__init__(sql_key)

#     def encryptInsertion(self, insert_request):
#         self.assureIsInsertionRequest(insert_request)
#         list_columns, list_values = self.getColumnsAndValues(insert_request)
#         dict_encryption = self.encryptValuesOfColumnsUsingAES(list_columns, list_values)
#         request_encrypted = self.replaceRequestByEncryptedValues(
#             insert_request, dict_encryption
#         )
#         return request_encrypted

#     def encryptManuallyInsertion(self, insert_request):
#         self.assureIsInsertionRequest(insert_request)
#         list_columns, list_values = self.getColumnsAndValues(insert_request)
#         dict_encryption = self.encryptValuesOfColumnsUsingCryptocode(
#             list_columns, list_values
#         )
#         request_encrypted = self.replaceRequestByEncryptedValues(
#             insert_request, dict_encryption
#         )
#         return request_encrypted

#     def assureIsInsertionRequest(self, insert_request):
#         if ("INSERT INTO" in insert_request) == False:
#             raise AttributeError(f"Not an insertion request: {insert_request}")

#     def getColumnsAndValues(self, insert_request):
#         tuples = re.findall("\(.*?\)", insert_request)

#         columns = tuples[0][1:-1]
#         list_columns = re.split(", ", columns)

#         values = tuples[1][1:-1]
#         values = re.sub("'", "", values)
#         list_values = re.split(", ", values)

#         return list_columns, list_values

#     def encryptValuesOfColumnsUsingAES(self, list_columns, list_values):
#         dict_replacement = {}
#         for column in list_columns:
#             i_col = list_columns.index(column)
#             value_unchanged = list_values[i_col]
#             if value_unchanged == "nan":
#                 dict_replacement[value_unchanged] = "NULL"
#             elif column not in self.list_columns_to_left_unchanged:
#                 value_encrypted = self.encryptValueUsingAES(value_unchanged)
#                 dict_replacement[value_unchanged] = value_encrypted
#             else:
#                 dict_replacement[value_unchanged] = value_unchanged
#         return dict_replacement

#     def encryptValuesOfColumnsUsingCryptocode(self, list_columns, list_values):
#         dict_replacement = {}
#         for column in list_columns:
#             i_col = list_columns.index(column)
#             value_unchanged = list_values[i_col]
#             if (column not in self.list_columns_to_left_unchanged) and (
#                 value_unchanged != "nan"
#             ):
#                 value_encrypted = self.encryptValueUsingCryptocode(value_unchanged)
#                 dict_replacement[value_unchanged] = value_encrypted
#             else:
#                 dict_replacement[value_unchanged] = value_unchanged
#         return dict_replacement

#     def encryptValueUsingAES(self, value):
#         encrypted_value = "AES_ENCRYPT('" + value + "', " + self.key + ")"
#         return encrypted_value

#     def decryptValueUsingAES(self, encrypted_value):
#         value = "AES_DECRYPT('" + encrypted_value + "', " + self.key + ")"
#         return value

#     def encryptValueUsingCryptocode(self, value):
#         # return cryptocode.encrypt(value, self.key)
#         return value

#     def decryptValueUsingCryptocode(self, value):
#         # return cryptocode.decrypt(value, self.key)
#         return value

#     def replaceRequestByEncryptedValues(self, request, dict_values_encrypted):
#         try:
#             for value in dict_values_encrypted.keys():
#                 encrypted = dict_values_encrypted[value]
#                 request = re.sub(value, encrypted, request)
#         except re.error:
#             logging.debug(f"value: {value}\nrequest:{request}")
#         return request
