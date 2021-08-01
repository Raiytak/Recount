import pymysql
import logging

import wrapper_dash.facilitator_dash.user_identification as user_identification


class SQLConnector:
    def __init__(self, db_config):
        self.DB_CONFIG = db_config
        self.connection, self.cursor = self._connect()

    def __enter__(self):
        # self.connection, self.cursor = self._connect()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self._end_connection()
        pass

    def _connect(self, db_config=None):
        if db_config == None:
            db_config = self.DB_CONFIG
        myConnection = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            passwd=db_config["password"],
            db=db_config["db"],
        )
        return myConnection, myConnection.cursor()

    def _end_connection(self):
        self.connection.close()


class WrapperOfTable(SQLConnector):
    def __init__(self, table, db_config):
        super().__init__(db_config)
        self.table = table

    def _execute(self, request_sql):
        request_sql = request_sql.replace("&", self.table)
        # print(request_sql)
        try:
            response = self.cursor.execute(request_sql)
        except pymysql.Error as err:
            print(f"Pymysql exception occured during request execution : {err}")
        else:
            return response
        return ""
        # username = user_identification.getUsername()
        # print(username)

    def select(self, request_sql):
        self._execute(request_sql)
        return self.cursor.fetchall()

    def selectRowId(self, id):
        request = "SELECT * FROM & WHERE ID = " + str(id)
        return self.select(request)

    def insert(self, request_sql):
        self._execute(request_sql)
        try:
            self.connection.commit()
        except Exception as exc:
            print(f"Exception during commit : '{exc}'")
            try:
                print("Trying a rollback ... ")
                self.connection.rollback()
                print("Rollback done!")
            except Exception as exc:
                print(f"Rollback failed : {str(exc)}")

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
        request = "DELETE FROM & where id = " + str(row_id)
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
        # request = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='"+database+"' AND TABLE_NAME='"+table+"'"
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
