import datetime
import unidecode

import numpy as np
import pandas as pd



class DataframeToSql():
    def translateDataframeToRequestSql(self, dataframe, equivalent_columns):
        dict_of_list_list = self.convertDataframeColumnsToDictOfListList(dataframe)
        list_requests_sql = self.convertDictListListToRequestSql(dict_of_list_list, equivalent_columns)
        return list_requests_sql
    
        
    def convertDataframeColumnsToDictOfListList(self, dataframe):
        dict_by_columns = {"len":len(dataframe)}
        list_columns = dataframe.columns
        for col in list_columns:
            dict_by_columns[col] = self._convertColumnValue(dataframe[col], col)
        return dict_by_columns
    
    def _convertColumnValue(self, dataframe_col, column):
        list_list_returned = [list(dataframe_col.apply(str))]
        return list_list_returned

    def convertDictListListToRequestSql(self, dict_list_list, dict_equivalent_columns):
        equivalent_columns = dict_equivalent_columns
        start_requests = ["INSERT INTO & ("]*dict_list_list["len"]
        end_requests = ["VALUES ("]*dict_list_list["len"]
        
        for column_excel in equivalent_columns.keys():
            columns_sql = equivalent_columns[column_excel]
            if column_excel == "ID": #Goal is to avoid a coma at the start of the request (try without the if and look at the requests to understand)
                values = dict_list_list[column_excel][0]
                dict_list_list_bool = [False if (values[i]==str(np.nan) or values[i]=="None") else True for i in range(len(values))]
                start_requests = self._concatenateRequestsAndValueWithoutComa(start_requests, columns_sql[0], dict_list_list_bool)
                end_requests = self._concatenateRequestsAndListValuesWithoutComa(end_requests, dict_list_list[column_excel][0], dict_list_list_bool)
            else:
                for i in range(len(columns_sql)):
                    values = dict_list_list[column_excel][i]
                    dict_list_list_bool = [False if (values[i]==str(np.nan) or values[i]=="None") else True for i in range(len(values))]
                    start_requests = self._concatenateRequestsAndValue(start_requests, columns_sql[i], dict_list_list_bool)
                    end_requests = self._concatenateRequestsAndListValues(end_requests, dict_list_list[column_excel][i],dict_list_list_bool)
                
        start_requests = self.closeRequest(start_requests)
        end_requests = self.closeRequest(end_requests)
            
        list_requests = self._concatenateRequestsAndList(start_requests, end_requests)
            
        return list_requests
            
    
    def _concatenateRequestsAndList(self, requests, values):
        return [requests[i]+" "+values[i] for i in range(len(requests))]
                
                
    def _concatenateRequestsAndValue(self, requests, column_sql, dict_list_list_bool):
        return [requests[i]+", "+column_sql if dict_list_list_bool[i] else requests[i] for i in range(len(requests))]
    
    def _concatenateRequestsAndListValues(self, requests, values, dict_list_list_bool):
        return [requests[i]+", '"+values[i]+"'" if dict_list_list_bool[i] else requests[i] for i in range(len(requests))]
    
                
    def _concatenateRequestsAndValueWithoutComa(self, requests, column_sql, dict_list_list_bool):
        return [requests[i]+column_sql if dict_list_list_bool[i] else requests[i] for i in range(len(requests))]
    
    def _concatenateRequestsAndListValuesWithoutComa(self, requests, values, dict_list_list_bool):
        return [requests[i]+"'"+values[i]+"'" if dict_list_list_bool[i] else requests[i] for i in range(len(requests))]
    
    
    def closeRequest(self, requests):
        return [requests[i] + ")" for i in range(len(requests))]


    