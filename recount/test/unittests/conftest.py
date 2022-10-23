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

from accessors.file_management import UserManager


USERNAME = "hello"
DB_CONFIG = {}
TABLE_NAME = Table.EXPENSE
EXPECTED_DEFAULT_COLUMNS_NAME = [
    "ID",
    "username",
    "date",
    "amount",
    "category",
    "travel",
    "company",
    "description",
    "payment_method",
]

USER_ACCESS = UserManager(USERNAME)
USER_TABLE = UserSqlTable(USERNAME, TABLE_NAME)

# USER_DATA_PIPELINE = pipeline.UserDataPipeline(USERNAME)
# USER_GRAPH_PIPELINE = pipeline.UserGraphPipeline(USERNAME)


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

