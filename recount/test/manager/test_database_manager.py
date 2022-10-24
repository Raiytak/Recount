from .conftest import *
from database_manager import DatabaseManager


def test_database_dataframe(database_manager: DatabaseManager):
    return
    TODO
    df = database_manager.dataframe(excel_1)
    data_json = df.to_json()
    # If broke the PATH_DF_OUTPUT_JSON_1, here is the way to recreate it
    # from accessors.file_management import FileAccessor, TestManager
    # FileAccessor.writeJson(TestManager.PATH_DF_OUTPUT_JSON_1, data_json)
    assert data_json == json_df_output_1
