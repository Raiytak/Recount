import pymysql


class SQLConnector():
    def __init__(self, config):
        self.myConnection, self.cursor = self.connect(config)


        
    def connect(self, config):
        # Line to change depending on the deployment method
        conf = config["mysql_linux"]
        myConnection = pymysql.connect( host=conf["host"],
                                       user=conf["user"],
                                       passwd=conf["passwd"],
                                       db=conf["db"])
        return myConnection, myConnection.cursor()
    
    def  end_connection(self):
        self.myConnection.close()



class WrapperOfTable(SQLConnector):
    def __init__(self, table, config):
        SQLConnector.__init__(self, config)
        self.table = table
        
        
    def _execute(self, request_sql):
        request_sql = request_sql.replace("&", self.table)
        response = self.cursor.execute(request_sql)
        return response
        
    def selectRowId(self, id):
        request = "SELECT * FROM & WHERE ID = "+str(id)
        return self.select(request)
    
    def select(self, request_sql):
        self._execute(request_sql)
        return self.cursor.fetchall()    
        
    def insertAllReqs(self, list_request_sql):
        for req_sql in list_request_sql:
            self.insert(req_sql)
        
    def insert(self, request_sql):
        self._execute(request_sql)
        self.myConnection.commit()
        if self.cursor.fetchall() != ():
            return Exception
    
    def deleteListRowsId(self, list_rows_id):
        for row_id in list_rows_id:
            self.deleteRowId(row_id)
    
    def deleteRowId(self, row_id):
        request = "DELETE FROM & where id = "+str(row_id)
        self._execute(request)
    
    def dumpTable(self):
        request = "DELETE FROM &"
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
        request = "SELECT column_name FROM information_schema.columns WHERE table_schema='"+database+"' AND table_name='"+table+"'" + " ORDER BY table_name, ordinal_position;"
        response = self.select(request)
        name_columns = [col[0] for col in response]
        return name_columns
