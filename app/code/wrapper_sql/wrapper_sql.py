import pymysql


class SQLConnector:
    def __init__(self, config):
        self.CONFIG = config

    def _connect(self, config=None):
        if config == None:
            config = self.CONFIG
        myConnection = pymysql.connect(
            host=config["host"],
            user=config["user"],
            passwd=config["passwd"],
            db=config["db"],
        )
        return myConnection, myConnection.cursor()

    def _end_connection(self):
        self.myConnection.close()


class WrapperOfTable(SQLConnector):
    def __init__(self, table, config):
        super().__init__(config)
        self.table = table

    def _execute(self, request_sql):
        self.myConnection, self.cursor = self._connect()

        request_sql = request_sql.replace("&", self.table)
        response = self.cursor.execute(request_sql)

        self._end_connection()
        return response

    def select(self, request_sql):
        self._execute(request_sql)
        return self.cursor.fetchall()

    def selectRowId(self, id):
        request = "SELECT * FROM & WHERE ID = " + str(id)
        return self.select(request)

    def insert(self, request_sql):
        self._execute(request_sql)
        self.myConnection.commit()
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
