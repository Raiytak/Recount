import numpy as np
import logging
import pdb


class Requestor:
    list_starting_req = []
    list_elem_req = []
    list_bool = []
    elem_decorator = ""


class DataframeToSql:
    def translateDataframeToInsertRequestSql(self, dataframe, equivalent_columns):
        # In the case where the dataframe is empty, we return an empty request
        if dataframe.empty == True:
            return [""]
        # dataframe = self.cleanDataframe(dataframe)
        dict_of_list = self.convertDataframeColumnsToDictOfListList(dataframe)
        list_requests_sql = self.convertDictListToInsertRequestSql(
            dict_of_list, equivalent_columns
        )
        return list_requests_sql

    def convertDataframeColumnsToDictOfListList(self, dataframe):
        dict_by_columns = {"len": len(dataframe)}
        list_columns = dataframe.columns
        for col in list_columns:
            dict_by_columns[col] = self.convertColumnValue(dataframe[col])
        return dict_by_columns

    def convertColumnValue(self, dataframe_col):
        list_returned = list(dataframe_col.apply(str))
        return list_returned

    def convertDictListToInsertRequestSql(
        self, dict_list_values, dict_equivalent_columns
    ):
        insert_into_req = ["INSERT INTO & ("] * dict_list_values["len"]
        values_req = ["VALUES ("] * dict_list_values["len"]

        for column_excel in dict_equivalent_columns.keys():
            column_sql = dict_equivalent_columns[column_excel]

            list_values = dict_list_values[column_excel]
            list_bool = self.boolListValuesNotNull(list_values)

            insert_requestor = Requestor()
            insert_requestor.list_starting_req = insert_into_req
            insert_requestor.list_elem_req = column_sql
            insert_requestor.list_bool = list_bool
            insert_requestor.elem_decorator = ""
            insert_into_req = self.concatenateRequestAndElement(insert_requestor)

            insert_requestor.list_starting_req = values_req
            insert_requestor.list_elem_req = list_values
            insert_requestor.list_bool = list_bool
            insert_requestor.elem_decorator = "'"
            values_req = self.concatenateRequestAndElement(insert_requestor)

        insert_into_req = self.closeRequest(insert_into_req)
        values_req = self.closeRequest(values_req)

        insert_into_req = self.removeFirstComa(insert_into_req)
        values_req = self.removeFirstComa(values_req)

        list_starting_req = self.concatenateRequestsAndList(insert_into_req, values_req)

        return list_starting_req

    def boolListValuesNotNull(self, list_values):
        bool_list_value_not_null = [
            False
            if (list_values[i] == str(np.nan) or list_values[i] == "None")
            else True
            for i in range(len(list_values))
        ]
        return bool_list_value_not_null

    def concatenateRequestsAndList(self, requests, values):
        return [requests[i] + " " + values[i] for i in range(len(requests))]

    def concatenateRequestAndElement(self, requestor):
        list_elem_req = requestor.list_elem_req
        list_bool = requestor.list_bool
        list_starting_req = requestor.list_starting_req
        decor = requestor.elem_decorator

        if len(list_elem_req) == 1:
            list_elem_req = list_elem_req * len(list_bool)
        return [
            list_starting_req[i] + ", " + decor + list_elem_req[i] + decor
            if list_bool[i]
            else list_starting_req[i]
            for i in range(len(list_starting_req))
        ]

    def closeRequest(self, requests):
        return [requests[i] + ")" for i in range(len(requests))]

    def removeFirstComa(self, requests):
        return [requests[i].replace(", ", "", 1) for i in range(len(requests))]
