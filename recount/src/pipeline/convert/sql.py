# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Convert dataframe to request SQL.
"""

import numpy as np
import pandas as pd

from com import SqlKeyword, SqlRequest

# TODO: test
class ResponseSqlToDataframe:
    def translateResponseSqlToDataframe(self, response_sql, wrapper_table):
        dataframe = pd.DataFrame(response_sql)
        columns_name = wrapper_table.getNameColumns()

        # If data exists in the period selected, the dataframe is not empty and can be returned by describing it's columns
        # Else we simply return the dataframe completely empty
        try:
            if dataframe.empty == False:
                dataframe.columns = columns_name
            else:
                pass
        except Exception(
            "Exception in response_to_dataframe.translateResponseSqlToDataframe"
        ):
            pass
        return dataframe

    def getEquivalentColumns(self, wrapper_table):
        columns_name = wrapper_table.getNameColumns()
        equivalent_columns = {col: [col] for col in columns_name}
        return equivalent_columns

    # Create a dataframe with empty values
    def getDataframeWithEmptyValues(self, wrapper_table):
        columns_name = wrapper_table.getNameColumns()
        import logging

        logging.info(columns_name)
        dataframe = pd.DataFrame(
            np.array([[0, "2000-01-01", 0, "", "alimentary", "", "", None, "", "", 0]]),
            columns=columns_name,
        )
        return dataframe


class ResponseSqlToList:
    def translateResponseSqlToList(self, response_sql):
        list_response = [elem[0] for elem in response_sql]
        return list_response


# TODO : use the SqlRequest to improve this class
class DataframeToSql:
    @classmethod
    def translateIntoInsertRequests(cls, dataframe, equivalent_columns, table_name):
        """In the case where the dataframe is empty, we return an empty request"""
        if dataframe.empty == True:
            return []

        list_rows = cls.translateDataframeTolist(dataframe)

        requests = [
            SqlRequest(
                SqlKeyword.INSERT,
                table_name,
                insert_columns=equivalent_columns.values(),
                insert_values=row,
            )
            for row in list_rows
        ]
        return requests

    @classmethod
    def translateDataframeTolist(cls, dataframe):
        def isNull(value):
            if type(value) == float:
                if np.isnan(value):
                    return True
            return False

        list_rows = dataframe.values.tolist()
        # TODO: Problem might come from here (truncate None values)
        cleaned_list = [
            [value for value in row if not isNull(value)] for row in list_rows
        ]
        return cleaned_list

    # def translateDataframeToUpdateRequestSql(self, dataframe, equivalent_columns):
    #     # In the case where the dataframe is empty, we return an empty request
    #     if dataframe.empty == True:
    #         return [""]
    #     # dataframe = self.cleanDataframe(dataframe)
    #     dict_of_list = self.convertDataframeColumnsToDictOfListList(dataframe)
    #     list_requests_sql = self.convertDictListToUpdateRequestSql(
    #         dict_of_list, equivalent_columns
    #     )
    #     return list_requests_sql

    # def convertDataframeColumnsToDictOfListList(self, dataframe):
    #     dict_by_columns = {"len": len(dataframe)}
    #     list_columns = dataframe.columns
    #     for col in list_columns:
    #         dict_by_columns[col] = self.convertColumnValue(dataframe[col])
    #     return dict_by_columns

    # def convertColumnValue(self, dataframe_col):
    #     list_returned = dataframe_col.apply(str).tolist()
    #     return list_returned

    # def convertDictListToInsertRequestSql(
    #     self, dict_list_values, dict_equivalent_columns
    # ):
    #     start_insert_into_reqs = ["INSERT INTO & ("] * dict_list_values["len"]
    #     start_values_reqs = ["VALUES ("] * dict_list_values["len"]

    #     insert_prerequestor = self.PreRequestor()
    #     insert_prerequestor.dict_list_values = dict_list_values
    #     insert_prerequestor.dict_equivalent_columns = dict_equivalent_columns
    #     insert_prerequestor.elem_decorator = ""
    #     insert_prerequestor.symbol = ""

    #     (
    #         insert_reqs_col,
    #         values_reqs_val,
    #     ) = self.loopConcatenateRequestAndElementsForInsert(insert_prerequestor)

    #     insert_into_reqs = self.concatenateListOfLists(
    #         start_insert_into_reqs, insert_reqs_col
    #     )
    #     values_reqs = self.concatenateListOfLists(start_values_reqs, values_reqs_val)

    #     list_reqs = self.concatenateListOfLists(insert_into_reqs, values_reqs)
    #     # logging.debug(list_reqs)
    #     return list_reqs

    # def convertDictListToUpdateRequestSql(
    #     self, dict_list_values, dict_equivalent_columns
    # ):
    #     start_update_reqs = ["UPDATE & SET"] * dict_list_values["len"]
    #     keys_to_keep = ["amount"]
    #     dict_eq_cols_reduced = self.newDictWithOnlyKeys(
    #         dict_equivalent_columns, keys_to_keep
    #     )

    #     update_prerequestor = self.PreRequestor()
    #     update_prerequestor.dict_list_values = dict_list_values
    #     update_prerequestor.dict_equivalent_columns = dict_eq_cols_reduced
    #     update_prerequestor.elem_decorator = "'"
    #     update_prerequestor.symbol = " = "

    #     update_reqs_val = self.loopConcatenateRequestAndElementsForUpdate(
    #         update_prerequestor
    #     )
    #     update_reqs = self.concatenateListOfLists(
    #         start_update_reqs, update_reqs_val, " "
    #     )

    #     start_condition_reqs = ["WHERE"] * dict_list_values["len"]
    #     keys_to_keep = ["username", "ID"]
    #     dict_eq_cols_condition = self.newDictWithOnlyKeys(
    #         dict_equivalent_columns, keys_to_keep
    #     )

    #     condition_prerequestor = self.PreRequestor()
    #     condition_prerequestor.dict_list_values = dict_list_values
    #     condition_prerequestor.dict_equivalent_columns = dict_eq_cols_condition
    #     condition_prerequestor.elem_decorator = "'"
    #     condition_prerequestor.symbol = " = "

    #     condition_reqs_val = self.loopConcatenateRequestAndElementsForUpdate(
    #         condition_prerequestor
    #     )
    #     condition_reqs = self.concatenateListOfLists(
    #         start_condition_reqs, condition_reqs_val, " "
    #     )

    #     list_reqs = self.concatenateListOfLists(update_reqs, condition_reqs, " ")
    #     # logging.debug(list_reqs)
    #     return list_reqs

    # def boolListValuesNotNull(self, list_values):
    #     bool_list_value_not_null = [
    #         str(False)
    #         if (list_values[i] == str(np.nan) or list_values[i] == "None")
    #         else str(True)
    #         for i in range(len(list_values))
    #     ]
    #     return bool_list_value_not_null

    # def concatenateListOfLists(self, list_A, list_B, joiner=""):
    #     list_A, list_B = self.multiplyElementsIfNecessary(list_A, list_B)
    #     return [list_A[i] + joiner + list_B[i] for i in range(len(list_A))]

    # def concatenateRequestAndElementUsingEmptyElemA(self, requestor):
    #     empty_list = [""]
    #     requestor.list_elem_A_req = empty_list
    #     return self.concatenateRequestAndElementsUsing(requestor)

    # def closeRequest(self, requests):
    #     return [requests[i] + ") " for i in range(len(requests))]

    # def removeFirstComa(self, requests):
    #     return [requests[i].replace(", ", "", 1) for i in range(len(requests))]

    # def newDictWithOnlyKeys(self, dict_to_clean, list_keys_to_keep):
    #     return {list_keys_to_keep[i]: dict_to_clean[i] for i in list_keys_to_keep}

    # def concatenateRequestAndElementsUsing(self, requestor):
    #     requestor = self.multiplyElementsOfRequestorIfNecessary(requestor)

    #     return [
    #         requestor.list_starting_req[i]
    #         + ", "
    #         + requestor.list_elem_A_req[i]
    #         + requestor.symbol
    #         + requestor.elem_decorator
    #         + requestor.list_elem_B_req[i]
    #         + requestor.elem_decorator
    #         if requestor.list_bool[i]
    #         else requestor.list_starting_req[i]
    #         for i in range(len(requestor.list_starting_req))
    #     ]

    # def multiplyElementsIfNecessary(self, listA, listB):
    #     if len(listA) == 1:
    #         listA = listA * len(listB)
    #     if len(listB) == 1:
    #         listB = listB * len(listA)
    #     return listA, listB

    # def multiplyElementsOfRequestorIfNecessary(self, requestor):
    #     requestor.list_elem_A_req, trash = self.multiplyElementsIfNecessary(
    #         requestor.list_elem_A_req, requestor.list_bool
    #     )
    #     requestor.list_elem_B_req, trash = self.multiplyElementsIfNecessary(
    #         requestor.list_elem_B_req, requestor.list_bool
    #     )
    #     requestor.list_starting_req, trash = self.multiplyElementsIfNecessary(
    #         requestor.list_starting_req, requestor.list_bool
    #     )
    #     return requestor

    # def loopConcatenateRequestAndElementsForInsert(self, pre_requestor):
    #     insert_into_reqs, values_reqs = [""], [""]
    #     insert_requestor = self.Requestor()
    #     value_requestor = self.Requestor()
    #     for column_excel in pre_requestor.dict_equivalent_columns.keys():
    #         column_sql = pre_requestor.dict_equivalent_columns[column_excel]

    #         list_values = pre_requestor.dict_list_values[column_excel]
    #         list_bool = self.boolListValuesNotNull(list_values)

    #         insert_requestor.length = len(list_bool)
    #         insert_requestor.elem_decorator = pre_requestor.elem_decorator
    #         insert_requestor.symbol = pre_requestor.symbol

    #         insert_requestor.list_starting_req = insert_into_reqs
    #         insert_requestor.list_elem_B_req = column_sql
    #         insert_requestor.list_bool = list_bool
    #         insert_into_reqs = self.concatenateRequestAndElementUsingEmptyElemA(
    #             insert_requestor
    #         )

    #         value_requestor.list_starting_req = values_reqs
    #         value_requestor.list_elem_B_req = list_values
    #         value_requestor.list_bool = list_bool
    #         value_requestor.elem_decorator = "'"
    #         values_reqs = self.concatenateRequestAndElementUsingEmptyElemA(
    #             value_requestor
    #         )

    #     insert_into_reqs = self.closeRequest(insert_into_reqs)
    #     values_reqs = self.closeRequest(values_reqs)

    #     insert_into_reqs = self.removeFirstComa(insert_into_reqs)
    #     values_reqs = self.removeFirstComa(values_reqs)

    #     return insert_into_reqs, values_reqs

    # def loopConcatenateRequestAndElementsForUpdate(self, pre_requestor):
    #     for column_excel in pre_requestor.dict_eq_cols_reduced.keys():
    #         column_sql = pre_requestor.dict_eq_cols_reduced[column_excel]

    #         list_values = pre_requestor.dict_list_values[column_excel]
    #         list_bool = self.boolListValuesNotNull(list_values)

    #         new_requestor = self.Requestor()
    #         new_requestor.length = len(list_bool)
    #         new_requestor.elem_decorator = pre_requestor.elem_decorator
    #         new_requestor.symbol = pre_requestor.symbol

    #         new_requestor.list_starting_req = update_reqs
    #         new_requestor.list_elem_A_req = column_sql
    #         new_requestor.list_elem_B_req = list_values
    #         update_reqs = self.concatenateRequestAndElementsUsing(new_requestor)

    #     update_reqs = self.closeRequest(update_reqs)
    #     update_reqs = self.removeFirstComa(update_reqs)

    #     return update_reqs
