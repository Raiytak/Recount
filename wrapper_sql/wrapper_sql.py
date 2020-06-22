import pymysql
import pandas as pd
import numpy as np




class SQLConnector():
    def __init__(self):
        self.hostname = 'localhost'
        self.username = 'root'
        self.password = ''
        self.database = 'depenses'
        
        self.myConnection, self.cursor = self.connect()
        
    def connect(self):
        myConnection = pymysql.connect( host=self.hostname,
                                       user=self.username,
                                       passwd=self.password,
                                       db=self.database )
        return myConnection, myConnection.cursor()
    
    def  end_connection(self):
        self.myConnection.close()



class WrapperOfTable(SQLConnector):
    def __init__(self, table):
        super().__init__()
        self.table = table
        
        
    def _execute(self, request_sql):
        request_sql = request_sql.replace("&", self.table)
        # print("_execute  : ", request_sql)
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
        request = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='"+database+"' AND TABLE_NAME='"+table+"'"
        response = self.select(request)
        name_columns = [col[0] for col in response]
        return name_columns



class ResponseSqlToDataframe():
    def translateResponseSqlToDataframe(self, response_sql, wrapper_table):
        dataframe = pd.DataFrame(response_sql)
        if dataframe.empty == True:
            return dataframe
        # dataframe = dataframe.replace(None, str(np.nan))
        columns_name = wrapper_table.getNameColumns()
        dataframe.columns = columns_name
        return dataframe

    def getEquivalentColumns(self, wrapper_table):
        columns_name = wrapper_table.getNameColumns()
        equivalent_columns = {col:[col] for col in columns_name}
        return equivalent_columns


        
class ResponseSqlToList():
    def translateResponseSqlToList(self, response_sql):
        list_response = [elem[0] for elem in response_sql]
        return list_response