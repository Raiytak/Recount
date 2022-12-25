from .conftest import *
from datetime import datetime
from database.sql_db import UserSqlTable
from database_manager import DatabaseManager


def test_database_manager_dataframe(
    database_manager: DatabaseManager,
    use_excel_1_in_db,
    excpected_response_database_dataframe_1,
):
    start_date = datetime(1900, 1, 1)
    end_date = datetime(2200, 1, 1)
    df = database_manager.dataframe(start_date, end_date)
    data_json = df.to_json()
    # If broke this test, here is the way to recreate its test file:
    # from accessors.file_management import FileAccessor, TestManager
    # FileAccessor.writeJson(TestManager.DATABASE_DATAFRAME_JSON_1, data_json)
    assert data_json == excpected_response_database_dataframe_1


def test_database_manager_save_dataframe(
    database_manager: DatabaseManager,
    user_table: UserSqlTable,
    cleaned_df_input_1: pd.DataFrame,
    excpected_response_database_save_dataframe_1,
):
    database_manager.saveDataframe(cleaned_df_input_1)
    df = user_table.selectAll()
    data_json = df.to_json()
    # If broke this test, here is the way to recreate its test file:
    # from accessors.file_management import FileAccessor, TestManager
    # FileAccessor.writeJson(TestManager.DATABASE_SAVE_DATAFRAME_1, data_json)
    assert data_json == excpected_response_database_save_dataframe_1
