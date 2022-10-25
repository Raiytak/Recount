import pytest

from file_management import FileAccessor, TestManager


@pytest.fixture
def json_pipeline_output_1():
    data_json = FileAccessor.readJson(filepath=TestManager.OUTPUT_PIPELINE_JSON_1)
    return data_json
