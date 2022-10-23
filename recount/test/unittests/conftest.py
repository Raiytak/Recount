import datetime
import pytest

# import json
# import pandas
# from unittest.mock import MagicMock, patch

from database.sql_db import (
    Table,
    SqlKeyword,
    SqlRequest,
    SqlTable,
    UserSqlTable,
)

# from accessors.file_management import UserManager


DB_CONFIG = {}

# USER_ACCESS = UserManager(username)
# @pytest.fixture
# def user_table(username, table_name):
#     user_table = UserSqlTable(username, table_name)
#     yield user_table
#     user_table.truncateTableOfUser()


# USER_DATA_PIPELINE = pipeline.UserDataPipeline(username)
# USER_GRAPH_PIPELINE = pipeline.UserGraphPipeline(username)


# ---
# Add param to a fixture
# @pytest.fixture
# def tester(request):
#     """Create tester object"""
#     return MyTester(request.param)


# class TestIt:
#     @pytest.mark.parametrize('tester', [['var1', 'var2']], indirect=True)
#     def test_tc1(self, tester):
#        tester.dothis()
#        assert 1
