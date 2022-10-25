import typing
import pytest
from datetime import datetime
import pandas as pd

from file_management import FileAccessor, TestManager


@pytest.fixture
def excpected_response_dataframe_save_dataframe_1():
    data_json = FileAccessor.pickleLoad(filepath=TestManager.DATABASE_SAVE_DATAFRAME_1)
    return data_json
