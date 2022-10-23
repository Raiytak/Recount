from .conftest import *
from src.excel_manager import ExcelManager


def test_excel_dataframe(excel_manager: ExcelManager, excel_1, json_df_output_json_1):
    df = excel_manager.dataframe(excel_1)
    data_json = df.to_json()
    # If broke the path_df_output_json_1, here is the way to recreate it
    # from src.accessors.file_management import FileAccessor, TestManager
    # FileAccessor.writeJson(TestManager.path_df_output_json_1, data_json)
    assert data_json == json_df_output_json_1
