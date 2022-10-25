import typing
from datetime import datetime
import pandas as pd

from database.sql_db import *
from interface.sql_interface import *


class DatabaseManager:
    def __init__(self, user_table: UserSqlTable):
        self.user_table = user_table

    def dataframe(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> pd.DataFrame:
        condition = convertDateToSqlCondition(start_date, end_date)
        request = SqlRequest(SqlKeyword.SELECT, Table.EXPENSE, "*", condition)
        df = self.user_table.select(request)
        return df

    def saveDataframe(self, df: pd.DataFrame, *args, **kwargs):
        rearranged_df = rearrangeDfColumns(df, EXCEL_COLUMNS)
        sql_requests = convertDfToSqlInsertRequests(
            rearranged_df, Table.EXPENSE, EXCEL_COLUMNS
        )
        for req in sql_requests:
            self.user_table.insert(req)
