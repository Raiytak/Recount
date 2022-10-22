import sys
import argparse
import logging

import sql_db


def testSqlConnection():
    sql_table = sql_db.SqlTable()
    print("**                       **")
    print("   Connection successful   ")
    print("Current database: '{}'".format(sql_table.database_name))
    print("Current table: '{}'".format(sql_table.table_name))
    print("Columns: '{}'".format(sql_table.columns_name))
    print("**                       **")


def testSqlTableExists():
    # TODO
    pass
    # sql_request = sql_db.SqlRequest(sql_db.SqlKeyword.DELETE, sql_db.Table.EXPENSE)
    # print(sql_request)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--test-sql-connection",
    help="connect to the sql database. Raise Exception if fails",
    action="store_true",
    default=False,
)
parser.add_argument(
    "--test-sql-table-exists",
    help="check if the table provided exists on the current sql db",
    action="store_true",
    default=False,
)

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

if args.test_sql_connection:
    testSqlConnection()

if args.test_sql_table_exists:
    testSqlTableExists()
