import numpy as np


class DataframeToSql:
    def translateDataframeToRequestSql(self, dataframe, equivalent_columns):
        # In the case where the dataframe is empty, we return an empty request
        if dataframe.empty == True:
            return [""]
        dict_of_list_list = self.convertDataframeColumnsToDictOfListList(dataframe)
        list_requests_sql = self.convertDictListListToRequestSql(
            dict_of_list_list, equivalent_columns
        )
        return list_requests_sql

    def convertDataframeColumnsToDictOfListList(self, dataframe):
        dict_by_columns = {"len": len(dataframe)}
        list_columns = dataframe.columns
        for col in list_columns:
            dict_by_columns[col] = self._convertColumnValue(dataframe[col], col)
        return dict_by_columns

    def _convertColumnValue(self, dataframe_col, column):
        list_list_returned = [list(dataframe_col.apply(str))]
        return list_list_returned

    def convertDictListListToRequestSql(self, dict_list_list, dict_equivalent_columns):
        equivalent_columns = dict_equivalent_columns
        insert_into_req = ["INSERT INTO & ("] * dict_list_list["len"]
        values_req = ["VALUES ("] * dict_list_list["len"]

        # TODO understand this function and simplify it
        for column_excel in equivalent_columns.keys():
            columns_sql = equivalent_columns[column_excel]
            if (
                columns_sql[0] == "username"
            ):  # Goal is to avoid a coma at the start of the request (try without the if and look at the requests to understand)
                values = dict_list_list[column_excel][0]
                dict_list_list_bool = [
                    False if (values[i] == str(np.nan) or values[i] == "None") else True
                    for i in range(len(values))
                ]
                insert_into_req = self._concatenateRequestsAndValueWithoutComa(
                    insert_into_req, columns_sql[0], dict_list_list_bool
                )
                values_req = self._concatenateRequestsAndListValuesWithoutComa(
                    values_req, dict_list_list[column_excel][0], dict_list_list_bool
                )
            else:
                for i in range(len(columns_sql)):
                    values = dict_list_list[column_excel][i]
                    dict_list_list_bool = [
                        False
                        if (values[i] == str(np.nan) or values[i] == "None")
                        else True
                        for i in range(len(values))
                    ]
                    insert_into_req = self._concatenateRequestsAndValueWithComa(
                        insert_into_req, columns_sql[i], dict_list_list_bool
                    )
                    values_req = self._concatenateRequestsAndListValuesWithComa(
                        values_req, dict_list_list[column_excel][i], dict_list_list_bool
                    )

        insert_into_req = self.closeRequest(insert_into_req)
        values_req = self.closeRequest(values_req)

        list_requests = self._concatenateRequestsAndList(insert_into_req, values_req)

        return list_requests

    def _concatenateRequestsAndList(self, requests, values):
        return [requests[i] + " " + values[i] for i in range(len(requests))]

    def _concatenateRequestsAndValue(self, requests, column_sql, dict_list_list_bool):
        if column_sql == "ID":
            return self._concatenateRequestsAndValueWithoutComa(
                requests, column_sql, dict_list_list_bool
            )
        else:
            return self._concatenateRequestsAndValueWithComa(
                requests, column_sql, dict_list_list_bool
            )

    # TODO not working
    def _concatenateRequestsAndListValues(self, requests, values, dict_list_list_bool):
        if column_sql == "ID":
            return self._concatenateRequestsAndListValuesWithoutComa(
                requests, column_sql, dict_list_list_bool
            )
        else:
            return self._concatenateRequestsAndListValuesWithComa(
                requests, column_sql, dict_list_list_bool
            )

    def _concatenateRequestsAndValueWithComa(
        self, requests, column_sql, dict_list_list_bool
    ):
        return [
            requests[i] + ", " + column_sql if dict_list_list_bool[i] else requests[i]
            for i in range(len(requests))
        ]

    def _concatenateRequestsAndValueWithoutComa(
        self, requests, column_sql, dict_list_list_bool
    ):
        return [
            requests[i] + column_sql if dict_list_list_bool[i] else requests[i]
            for i in range(len(requests))
        ]

    def _concatenateRequestsAndListValuesWithComa(
        self, requests, values, dict_list_list_bool
    ):
        return [
            requests[i] + ", '" + values[i] + "'"
            if dict_list_list_bool[i]
            else requests[i]
            for i in range(len(requests))
        ]

    def _concatenateRequestsAndListValuesWithoutComa(
        self, requests, values, dict_list_list_bool
    ):
        return [
            requests[i] + "'" + values[i] + "'"
            if dict_list_list_bool[i]
            else requests[i]
            for i in range(len(requests))
        ]

    def closeRequest(self, requests):
        return [requests[i] + ")" for i in range(len(requests))]
