from unittest.mock import MagicMock, patch
import datetime
import pytest
import json
import pandas


from src import *
from src import website


USERNAME = "hello"
DB_CONFIG = {}
TABLE_NAME = Table.EXPENSE

USER_ACCESS = UserFilesAccess(USERNAME)
USER_TABLE = UserSqlTable(USERNAME, TABLE_NAME)

USER_DATA_PIPELINE = pipeline.UserDataPipeline(USERNAME)
USER_GRAPH_PIPELINE = pipeline.UserGraphPipeline(USERNAME)


def defaultSelectExpenseResponses(request):
    if (
        str(request)
        == "SELECT * FROM expense WHERE date >= '2019-09-02' AND date <= '2019-09-03' AND username='hello';"
    ):
        return (
            (
                60,
                "hello",
                datetime.date(2019, 9, 3),
                7.0,
                "leasure:pub",
                None,
                "pub universitaire",
                "soiree",
                "card",
            ),
            (
                61,
                "hello",
                datetime.date(2019, 9, 3),
                57.57,
                "alimentary:food",
                None,
                "metro",
                "nourriture",
                "card",
            ),
        )
    return ()

