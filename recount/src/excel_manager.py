import typing
from pathlib import Path
import pandas as pd

from accessors.file_management import UserManager
from interface.excel_interface import *


class ExcelManager:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def dataframe(
        self, filepath: Path = None, filename: str = None
    ) -> typing.Type[pd.DataFrame]:
        excel_data = self.user_manager.excel(filepath, filename)
        # TODO: add translation of columns using the SQL columns
        df = dfFromData(excel_data)
        return df

    def saveDataframe(self, df: pd.DataFrame, *args, **kwargs):
        excel_data = dataFromDf(df)
        self.user_manager.saveExcel(excel_data, *args, **kwargs)
