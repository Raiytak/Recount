import argparse
import sys

from src.accessors.file_management import TestManager, UserManager
from src.excel_manager import ExcelManager
from src.database.sql_db import Table, UserSqlTable
from src.database_manager import DatabaseManager
from src.pipeline.pipeline import cleanDf


parser = argparse.ArgumentParser()
parser.add_argument(
    "--populate-hello",
    help="populate the database with example for user hello",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--truncate-hello",
    help="remove data of user from the database",
    action="store_true",
    default=False,
)

args = parser.parse_args()

# -- Verifications --
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)


# -- Actions --
username = "hello"
user_manager = UserManager(username)
excel_manager = ExcelManager(user_manager)
user_table = UserSqlTable(username, Table.EXPENSE)
database_manager = DatabaseManager(user_table)

if args.populate_hello:

    df = excel_manager.dataframe(filepath=TestManager.EXCEL_1)
    cleaned_df = cleanDf(df, False)
    database_manager.saveDataframe(cleaned_df)


if args.truncate_hello:
    user_table.truncateUserOfTable()
