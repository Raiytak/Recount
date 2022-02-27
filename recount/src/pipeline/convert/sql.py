# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Convert dataframe to request SQL.
"""

import pandas as pd
from typing import List

from com import SqlKeyword, SqlRequest


def translateDataframeIntoInsertRequests(dataframe, table) -> List[SqlRequest]:
    """In the case where the dataframe is empty, we return an empty request"""
    if dataframe.empty == True:
        return []

    records = dataframe.to_dict(orient="records")

    requests = [
        SqlRequest(
            SqlKeyword.INSERT, table=table.table_name, insert_dict_values=record,
        )
        for record in records
    ]
    return requests


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

    # # Create a dataframe with empty values
    # def getDataframeWithEmptyValues(self, wrapper_table):
    #     columns_name = wrapper_table.getNameColumns()
    #     import logging

    #     logging.info(columns_name)
    #     dataframe = pd.DataFrame(
    #         np.array([[0, "2000-01-01", 0, "", "alimentary", "", "", None, "", "", 0]]),
    #         columns=columns_name,
    #     )
    #     return dataframe
