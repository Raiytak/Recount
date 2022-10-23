import typing
from datetime import datetime
import pandas as pd

from database.sql_db import UserSqlTable
from interface.sql_interface import *


class DatabaseManager:
    def __init__(self, user_table: UserSqlTable):
        self.user_table = user_table

    def dataframe(
        self, start_date: datetime, end_date: datetime
    ) -> typing.Type[pd.DataFrame]:
        pass

    def saveDataframe(self, df: pd.DataFrame, *args, **kwargs):
        pass
