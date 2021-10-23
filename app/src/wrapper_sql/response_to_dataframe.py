# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Convert the SQL responses to dataframes or list. 
It is also used to set the right column names.
"""

import pandas as pd
import numpy as np


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
        dataframe = pd.DataFrame(
            np.array([[0, "2000-01-01", 0, "", "no-data", "", "", None, "", "", 0]]),
            columns=columns_name,
        )
        return dataframe


class ResponseSqlToList:
    def translateResponseSqlToList(self, response_sql):
        list_response = [elem[0] for elem in response_sql]
        return list_response
