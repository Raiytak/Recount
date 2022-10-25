import typing
from datetime import datetime
import pandas as pd

from recount.src.database.sql_db import SqlKeyword, SqlRequest, Table

from .default import *


def convertDateToSqlCondition(
    start_date: datetime = None, end_date: datetime = None
) -> str:
    """
    start_date < SELECTION < end_date
    """
    if not (start_date or end_date):
        raise AttributeError("no date provided")
    if start_date and end_date:
        condition = start_date + " AND " + end_date
    if start_date:
        condition = start_date
    if end_date:
        condition = end_date
    return condition


def rearrangeDfColumns(df: pd.DataFrame, columns: typing.List[str]):
    rearranged_df = df[columns]
    return rearranged_df


def convertDfToSqlInsertRequests(
    df: pd.DataFrame, table: typing.Type[Table], columns: typing.List[str],
) -> typing.List[SqlRequest]:
    sql_requests = []
    for index, row in df.iterrows():
        values = list(row.values)
        sql_request = SqlRequest(
            SqlKeyword.INSERT, table, insert_columns=columns, insert_values=values,
        )
        sql_requests.append(sql_request)
    return sql_requests
