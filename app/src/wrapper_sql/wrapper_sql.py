# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Creation and management of the MySQL connections, requests and return the responses.
"""

import pymysql
from threading import Lock
import logging

from accessors.data_encryption import SqlEncryption


class SQLConnector:
    """Create and manage a connection to the MySQL database"""

    # TODO: Use Lock to serialize the requests
    # TODO: better management of the creation and deletion
    #       of the SQLConnectors instancitaions
    connection = None
    cursor = None
    co_lock = Lock()

    def __init__(self, db_config):
        self.DB_CONFIG = db_config
        self.connection, self.cursor = self._connect()
        self.SqlEncryption = SqlEncryption()

    def __enter__(self):
        self.co_lock.acquire()
        # self.connection, self.cursor = self._connect()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._end_connection()
        pass

    def _connect(self, db_config=None):
        # self.co_lock.acquire()
        if db_config == None:
            db_config = self.DB_CONFIG
        myConnection = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            passwd=db_config["password"],
            db=db_config["db"],
            ssl={"fake_flag_to_enable_tls": True},
        )
        return myConnection, myConnection.cursor()

    def _end_connection(self):
        # self.connection.close()
        self.co_lock.release()


class WrapperOfTable(SQLConnector):
    """Access to one table of the """

    def __init__(self, table, db_config):
        super().__init__(db_config)
        self.table = table

    def _execute(self, request_sql):
        request_sql = request_sql.replace("&", self.table)
        if request_sql == "":
            return ""
        try:
            response = self.cursor.execute(request_sql)
        except pymysql.Error as err:
            logging.exception(
                f"Pymysql exception occured during request execution\nRequest : {request_sql}\nError : \n{err}"
            )
        else:
            return response
        return ""

    def select(self, request_sql):
        # logging.debug(request_sql)
        self._execute(request_sql)
        return self.cursor.fetchall()

    def selectListRowId(self, list_ids):
        list_responses = []
        for id in list_ids:
            list_responses.append(self.selectRowId(id)[0])
        return list_responses

    def selectRowId(self, id):
        request = "SELECT * FROM & WHERE ID = " + str(id)
        return self.select(request)

    def insert(self, request_sql):
        # The encryption is taking too long, commented for now
        # encrypted_insertion = self.SqlEncryption.encryptInsertion(request_sql)

        # logging.debug(request_sql)
        # logging.debug(encrypted_insertion)
        self._execute(request_sql)
        try:
            self.connection.commit()
        except Exception as exc:
            logging.exception(f"Exception during commit : '{exc}'")
            try:
                logging.exception("Trying a rollback ... ")
                self.connection.rollback()
                logging.exception("Rollback done!")
            except Exception as exc:
                logging.exception(f"Rollback failed : {str(exc)}")

        response = self.cursor.fetchall()
        if response != ():
            return ValueError(f"SQL insertion error : {response}")

    def insertAllReqs(self, list_request_sql):
        for req_sql in list_request_sql:
            self.insert(req_sql)

    def deleteListRowsId(self, list_rows_id):
        for row_id in list_rows_id:
            self.deleteRowId(row_id)

    def deleteRowId(self, row_id):
        request = "DELETE FROM & where ID = " + str(row_id)
        self._execute(request)

    def dumpTable(self):
        request = "DELETE FROM &"
        self._execute(request)

    def dumpTableForUser(self, username):
        request = "DELETE FROM & WHERE username = " + "'" + username + "'"
        self._execute(request)

    def getNameDatabase(self):
        request = "SELECT DATABASE()"
        response = self.select(request)
        return response[0][0]

    def getNameTable(self):
        return self.table

    def getNameColumns(self):
        database = self.getNameDatabase()
        table = self.getNameTable()
        request = (
            "SELECT column_name FROM information_schema.columns WHERE table_schema='"
            + database
            + "' AND table_name='"
            + table
            + "'"
            + " ORDER BY table_name, ordinal_position;"
        )
        response = self.select(request)
        name_columns = [col[0] for col in response]
        return name_columns
