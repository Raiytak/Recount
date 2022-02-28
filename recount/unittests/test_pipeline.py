from .__init__ import *

import pytest
import json

from access.access_files import UnittestFilesAccess
import pipeline
import pipeline.convert as convert
from com.sql import UserSqlTable, Table


user_table = UserSqlTable(USERNAME, TABLE_NAME)


@pytest.mark.parametrize(("df", "expected"), UnittestFilesAccess.pipeline_test_values)
def test_pipeline_process(df, expected):
    usr_pipeline = pipeline.UpdateDatabase(USERNAME)
    usr_pipeline.cleanDataframe(df)
    pipeline_json = df.to_json()
    cleaned_json = json.loads(pipeline_json)
    assert cleaned_json == expected
    # Use to update the test file
    # with open(expected, "w", encoding="utf-8") as file:
    #     json.dump(cleaned_json, file, indent=4)


@pytest.mark.parametrize(("df", "expected"), UnittestFilesAccess.convert_test_values)
def test_translate_df_to_sql_requests(df, expected):
    usr_pipeline = pipeline.UpdateDatabase(USERNAME)
    usr_pipeline.cleanDataframe(df)
    requests = convert.translateDataframeIntoInsertRequests(df, user_table)
    for request, exp in zip(requests, expected):
        assert str(request) == exp
    # Use to update the test file
    # with open(expected, "w") as file:
    #     text = "\n".join([str(req) for req in requests])
    #     file.write(text)
