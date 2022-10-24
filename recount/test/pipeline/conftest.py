import pytest

from file_management import FileAccessor, TestManager


@pytest.fixture
def output_pipeline_json_1():
    return TestManager.PATH_DF_OUTPUT_PIPELINE_JSON_1


@pytest.fixture
def json_pipeline_output_1(output_pipeline_json_1):
    data_json = FileAccessor.readJson(filepath=output_pipeline_json_1)
    return data_json
