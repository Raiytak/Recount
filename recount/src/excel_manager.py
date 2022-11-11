import typing
from pathlib import Path
import pandas as pd

from accessors.file_management import UserManager
from interface.excel_interface import *

# from interface.excel_interface import convertDataframeToBytes
from pipeline.cleaner import removeColumnsNotInExpectedExcelColumns


class ExcelManager:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def dataframe(
        self, filepath: Path = None, filename: str = None
    ) -> typing.Type[pd.DataFrame]:
        excel_data = self.user_manager.excel(filepath, filename)
        # TODO: add translation of columns using the SQL columns
        df = dfFromData(excel_data)
        removeColumnsNotInExpectedExcelColumns(df, True)
        return df

    def saveDataframe(self, df: typing.Type[pd.DataFrame], *args, **kwargs):
        excel_data = dataFromDf(df)
        self.user_manager.saveExcel(excel_data, *args, **kwargs)

    def saveImportedExcel(self, imported_file, *args, **kwargs):
        content_type, buffer_content = decodeImportedFile(imported_file)
        excel_data = buffer_content.read()
        if not content_type == "xlsx":
            raise AttributeError(
                "provdided file is not 'xlsx' but {}".format(content_type)
            )
        self.user_manager.saveExcel(excel_data, *args, **kwargs)

    def getDefaultExcel(self) -> typing.Type[pd.DataFrame]:
        df = self.dataframe(self.user_manager.EXAMPLE_EXCEL, filename=None)
        return df
