# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Convert dataframe to request SQL.
"""

import numpy as np
import pandas as pd

from com import SqlKeyword, SqlRequest


# TODO: test
class DataframeToSql:
    def __init__(self, equivalent_columns):
        self.equivalent_columns = equivalent_columns

    # TODO: Test
    def translateDataframeIntoInsertRequests(self, dataframe, table):
        """In the case where the dataframe is empty, we return an empty request"""
        if dataframe.empty == True:
            return []

        sql_columns = table.columns_name
        excel_columns = [self.equivalent_columns[col] for col in sql_columns]
        rows = self.extractRows(dataframe, excel_columns)

        requests = [
            SqlRequest(
                SqlKeyword.INSERT,
                table.table_name,
                insert_columns=sql_columns,
                insert_values=row,
            )
            for row in rows
        ]
        return requests

    def extractRows(self, dataframe, columns: list) -> list:
        selection = dataframe.loc[:, columns]
        return selection.tolist()


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
