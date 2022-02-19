from unittest.mock import Mock
import pytest
import json

from access.access_files import UnittestFilesAccess
import pipeline

USERNAME = "hello"


@pytest.mark.parametrize(("input", "expected"), UnittestFilesAccess.pipeline_test_files)
def test_pipeline_process(input, expected):
    usr_pipeline = pipeline.UpdatePipeline(USERNAME)
    usr_pipeline.cleanDataframe(input)
    pipeline_json = input.to_json()
    cleaned_json = json.loads(pipeline_json)
    assert cleaned_json == expected
