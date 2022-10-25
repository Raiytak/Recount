from .conftest import *
from database.sql_db import UserSqlTable
from database_manager import DatabaseManager


# def test_database_dataframe(
#     database_manager: DatabaseManager, start_date: datetime, end_date: datetime
# ):
#     df = database_manager.dataframe(start_date, end_date)
#     data_json = df.to_json()
#     # If broke the PATH_DF_OUTPUT_JSON_1, here is the way to recreate it
#     # from accessors.file_management import FileAccessor, TestManager
#     # FileAccessor.writeJson(TestManager.PATH_DF_OUTPUT_JSON_1, data_json)
#     assert data_json == None


def test_database_save_dataframe(
    database_manager: DatabaseManager,
    user_table: UserSqlTable,
    cleaned_df_input_1: pd.DataFrame,
    excpected_response_dataframe_save_dataframe_1,
):
    database_manager.saveDataframe(cleaned_df_input_1)
    response = user_table.selectAll()
    # If broke this test, here is the way to recreate its test file:
    # from accessors.file_management import FileAccessor, TestManager
    # FileAccessor.pickleDump(TestManager.DATABASE_SAVE_DATAFRAME_1, response)
    assert response == excpected_response_dataframe_save_dataframe_1

