import sys
import argparse

from .main import *


parser = argparse.ArgumentParser()
parser.add_argument(
    "--test-sql-connection",
    help="connect to the sql database. Raise Exception if fails",
    action="store_true",
    default=False,
)
# parser.add_argument(
#     "--test-sql-table-exists",
#     help="check if the table provided exists on the current sql db",
#     action="store_true",
#     default=False,
# )

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

if args.test_sql_connection:
    testSqlConnection()

# if args.test_sql_table_exists:
#     testSqlTableExists()
