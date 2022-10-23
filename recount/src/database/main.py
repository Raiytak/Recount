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
