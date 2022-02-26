import pytest
import json

from access.access_files import UnittestFilesAccess
import pipeline


from .__init__ import *


@pytest.mark.parametrize(
    ("input", "expected"), UnittestFilesAccess.pipeline_test_values
)
def test_pipeline_process(input, expected):
    usr_pipeline = pipeline.UpdatePipeline(USERNAME)
    usr_pipeline.cleanDataframe(input)
    pipeline_json = input.to_json()
    cleaned_json = json.loads(pipeline_json)
    assert cleaned_json == expected
