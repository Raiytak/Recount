import typing
import pytest
from datetime import datetime
import pandas as pd
import json

from file_management import FileAccessor, TestManager


@pytest.fixture
def excpected_response_database_dataframe_1():
    data_json = FileAccessor.readJson(filepath=TestManager.DATABASE_DATAFRAME_JSON_1)
    return data_json


@pytest.fixture
def excpected_response_database_save_dataframe_1():
    data_json = FileAccessor.readJson(filepath=TestManager.DATABASE_SAVE_DATAFRAME_1)
    return data_json
