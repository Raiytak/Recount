from .conftest import *

from pipeline.pipeline import cleanDf


def test_excel_cleaner(df_input_1, json_pipeline_output_1):
    cleaned_df = cleanDf(df_input_1, inplace=False)
    data_json = cleaned_df.to_json()
    # If broke the PATH_DF_OUTPUT_PIPELINE_JSON_1, here is the way to recreate it
    # from accessors.file_management import FileAccessor, TestManager
    # FileAccessor.writeJson(TestManager.PATH_DF_OUTPUT_PIPELINE_JSON_1, data_json)
    assert data_json == json_pipeline_output_1


# from access.access_files import UnittestFiles


# @pytest.mark.parametrize(("df", "expected"), UnittestFiles.pipeline_test_values)
# def test_pipeline_process(df, expected):
#     USER_DATA_PIPELINE.cleanDataframe(df)
#     pipeline_json = df.to_json()
#     cleaned_json = json.loads(pipeline_json)
#     assert cleaned_json == expected
#     # Use to update the test file
#     # with open(expected, "w", encoding="utf-8") as file:
#     #     json.dump(cleaned_json, file, indent=4)


# # @pytest.mark.parametrize(
# #     ("start_date", "end_date", "expected"), ["2019-09-02", "2019-09-03", None]
# # )
# # def test_translate_df_to_sql_requests(start_date, end_date, expected):
# #     USER_DATA_PIPELINE = pipeline.UserGraphPipeline(username)
# #     dataframe = USER_DATA_PIPELINE.getDataframeForDate()
# #     breakpoint()
# #     for request, exp in zip(requests, expected):
# #         assert str(request) == exp
# #     # Use to update the test file
# #     with open(expected, "w") as file:
# #         text = "\n".join([str(req) for req in requests])
# #         file.write(text)
