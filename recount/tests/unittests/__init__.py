from src import *


USERNAME = "hello"
DB_CONFIG = {}
TABLE_NAME = Table.EXPENSE

# TODO: Mock sql connections
USER_ACCESS = UserFilesAccess(USERNAME)
USER_TABLE = UserSqlTable(USERNAME, TABLE_NAME)
USER_DATA_PIPELINE = pipeline.DataPipeline(USERNAME)
USER_GRAPH_PIPELINE = pipeline.GraphPipeline(USERNAME)
