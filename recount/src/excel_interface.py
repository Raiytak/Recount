import typing
from pathlib import Path
import pandas as pd

from accessors.file_management import UserManager
from interfaces.excel_interface import dfFromData


class UserExcelManager:
    def __init__(self, username: str, key: typing.Union[bytes, str] = None):
        self.username = username
        self.key = key
        self.user_manager = UserManager(self.username, self.key)

    def dataframe(self, filepath: Path = None) -> typing.Type[pd.DataFrame]:
        excel_data = self.user_manager.excel(filepath)
        # TODO: add translation of columns using the SQL columns
        df = dfFromData(excel_data)
        return df

    def saveExcel(self, data: bytes, name: str = None, *args, **kwargs):
        self.user_manager.saveExcel(data, name, *args, **kwargs)
