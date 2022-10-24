from .conftest import *
from src.excel_manager import ExcelManager


def test_excel_dataframe(excel_manager: ExcelManager, excel_1, json_df_output_1):
    df = excel_manager.dataframe(excel_1)
    data_json = df.to_json()
    # If broke the PATH_DF_OUTPUT_JSON_1, here is the way to recreate it
    # from accessors.file_management import FileAccessor, TestManager
    # FileAccessor.writeJson(TestManager.PATH_DF_OUTPUT_JSON_1, data_json)
    assert data_json == json_df_output_1
