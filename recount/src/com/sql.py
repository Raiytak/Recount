# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Creation and management of the MySQL connections, requests and return the responses.
"""

import logging
from enum import Enum
from typing import Union, List
from threading import Lock
import pymysql
import weakref

from access.access_files import AccessConfig, classproperty


class SqlSocket:
    """Create and manage a connection to the MySQL database"""

    def __init__(self, db_config=None):
        self.connection, self.cursor = self.createSocket(db_config)

    def createSocket(self, db_config):
        if db_config is None:
            db_config = AccessConfig.databaseConfig
        new_socket = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            passwd=db_config["password"],
            db=db_config["db"],
            ssl={"fake_flag_to_enable_tls": True},
        )
        return new_socket, new_socket.cursor()


class SqlManagerSingleton:
    """If a manager already exists for the provided
    db_config, returns it.
    Else instanciate a new manager for the db_config."""

    _instances = set()

    def __new__(cls, db_config=None):
        if cls.instance_alread_exists(db_config):
            return cls.get_instance_named(db_config)
        return super(SqlManagerSingleton, cls).__new__(cls)

    def __init__(self, db_config):
        self.db_config = db_config
        self._instances.add(weakref.ref(self))

    @classproperty
    def instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    @classmethod
    def instance_alread_exists(cls, db_config):
        return any(db_config == instance.db_config for instance in cls.instances)

    @classmethod
    def get_instance_named(cls, db_config):
        return next(
            instance for instance in cls.instances if db_config == instance.db_config
        )


class SqlSocketManager(SqlManagerSingleton):
    """Create and manage a connection to MySQL database."""

    # TODO : add test socket, restore socket, function to access socket

    def __init__(self, db_config=None):
        super().__init__(db_config)
        self.sql_socket = SqlSocket()
        self.lock = Lock()
        self._instances.add(weakref.ref(self))

    def __enter__(self) -> SqlSocket:
        self.lock.acquire()
        return self.sql_socket

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()


class SqlKeyword(Enum):
    SELECT = "SELECT"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
    INSERT = "INSERT INTO"

    FROM = "FROM"
    WHERE = "WHERE"
    ORDER = "ORDER BY"
    GROUP = "GROUP BY"
    SET = "SET"
    LIMIT = "LIMIT"
    VALUES = "VALUES"


class SqlRequest:
    # TODO: work the clean and is empty properties
    def __init__(
        self,
        action: SqlKeyword,
        table: str = None,
        column: Union[str, List[str]] = None,  # TODO: make the case list
        condition: str = None,
        username: str = None,
        group: str = None,
        order: str = None,
        limit: str = None,
        change: str = None,
        insert_columns: Union[tuple, list] = (),
        insert_values: Union[tuple, list] = (),
        by_hand: str = None,
    ) -> None:
        """
        :arg by_hand: useful to specify by hand the request, except for 'action' and 'table'
        """
        self.action = action.value if type(action) is SqlKeyword else action
        self.table_name = (
            self.concatenateIfValueNotNone(table, SqlKeyword.FROM.value + " ")
            if (not action == SqlKeyword.UPDATE) and (not action == SqlKeyword.INSERT)
            else table
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
        self.insert_columns = self.concatenateIfValueNotNone(
            self.concatenateOrNone(*insert_columns, joint=", "), "(", ")"
        )
        # TODO: add assert len(insert_columns) == len(insert_values)
        #       compare insert_columns to SqlTable columns
        insert_values = (
            ["'" + str(value) + "'" for value in insert_values]
            if not insert_values is None
            else insert_values
        )
        self.insert_values = self.concatenateIfValueNotNone(
            self.concatenateOrNone(*insert_values, joint=", "),
            f"{SqlKeyword.VALUES.value} (",
            ")",
        )
        self.by_hand = by_hand
        # if not self.is_clean:
        #     raise ArgumentError(
        #         "The constructed SqlRequest was provided wrongful arguments"
        #         + " and could not be instanciated properly"
        #     )

    def __str__(self) -> str:  # TODO : replace & by tables, or not
        if self.action == SqlKeyword.SELECT.value:
            return self.createSelectRequest()
        elif self.action == SqlKeyword.UPDATE.value:
            return self.createUpdateRequest()
        elif self.action == SqlKeyword.INSERT.value:
            return self.createInsertRequest()
        elif self.action == SqlKeyword.DELETE.value:
            return self.createDeleteRequest()
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

    # TODO: add test
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

    # @property
    # def is_clean(self) -> bool:
    #     if self.is_empty:
    #         return False
    #     return True

    # @property
    # def is_empty(self) -> bool:
    #     if (self.action is None) or (self.table_name is None):
    #         return True
    #     return False


class SqlTable:
    """Access to one table of the """

    # TODO : assert table exists
    def __init__(self, table_name, db_config: dict = None):
        self.table_name = table_name
        self.db_config = db_config

    def _execute(self, sql_request: SqlRequest, sql_socket: SqlSocket):
        # The encryption is taking too long, commented for now
        # encrypted_insertion = self.SqlEncryption.encryptInsertion(sql_request)

        # logging.debug(sql_request)
        # logging.debug(encrypted_insertion)
        request = str(sql_request)
        try:
            response = sql_socket.cursor.execute(request)
        except pymysql.Error as err:
            logging.exception(
                f"Pymysql exception occured during request execution\nRequest : {request}\nError : \n{err}"
            )
            return ""
        else:
            return response

    def select(self, sql_request: SqlRequest):
        with SqlSocketManager(self.db_config) as sql_socket:
            self._execute(sql_request, sql_socket)
            return sql_socket.cursor.fetchall()

    def insert(self, sql_request: SqlRequest):
        with SqlSocketManager(self.db_config) as sql_socket:
            self._execute(sql_request, sql_socket)
            try:
                sql_socket.connection.commit()
            except Exception as exc:
                logging.info(f"Exception during commit : '{exc}'")
                try:
                    logging.warning("Trying a rollback ... ")
                    sql_socket.connection.rollback()
                    logging.warning("Rollback done!")
                except Exception as exc:
                    logging.warning(f"Rollback failed : '{str(exc)}'")

            response = sql_socket.cursor.fetchall()
            if response != ():
                return ValueError(f"SQL insertion error : '{response}'")

    def delete(self, sql_request: SqlRequest):
        with SqlSocketManager(self.db_config) as sql_socket:
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
            table="information_schema.columns",
            condition=f"table_schema='{self.database_name}' AND table_name='{self.table_name}'",
            order="table_name, ordinal_position",
        )
        response = self.select(request)
        name_columns = [col[0] for col in response]
        return name_columns

    def selectAll(self):
        request = SqlRequest(
            action=SqlKeyword.SELECT, column="*", table=self.table_name
        )
        return self.select(request)

    def dumpTable(self):
        request = SqlRequest(action=SqlKeyword.DELETE, table=self.table_name)
        self.delete(request)


class UserSqlTable(SqlTable):
    def __init__(self, username: str, table_name: str, db_config: dict = None):
        super().__init__(table_name, db_config)
        self.username = username

    def selectAll(self):
        request = SqlRequest(
            action=SqlKeyword.SELECT,
            column="*",
            table=self.table_name,
            username=self.username,
        )
        return self.select(request)

    def dumpTable(self):
        request = SqlRequest(
            action=SqlKeyword.DELETE, table=self.table_name, username=self.username
        )
        self.delete(request)

    def selectRowId(self, id):
        request = SqlRequest(
            action=SqlKeyword.SELECT,
            table=self.table_name,
            condition=f"ID = {str(id)}",
            username=self.username,
        )
        return self.select(request)

    def insertAllReqs(self, list_request_sql):
        for req_sql in list_request_sql:
            self.insert(req_sql)

    # def selectListRowId(self, list_ids):
    #     return [self.selectRowId(id)[0] for id in list_ids]

    # def deleteListRowsId(self, list_rows_id):
    #     for row_id in list_rows_id:
    #         self.deleteRowId(row_id)


# import re


# class SqlEncryption:
#     """Encryption logic of the SQL exchanges."""

#     def __init__(self):
#         self.AccessConfig = AccessConfig()
#         sql_key = self.AccessConfig.getDataSqlKey()
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
