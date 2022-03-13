# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Convert dataframe to request SQL.
"""

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
