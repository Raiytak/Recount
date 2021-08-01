from accessors.access_config import AccessConfig

myAccessConfig = AccessConfig()
db_config = myAccessConfig.getDatabaseConfig()


from wrapper_sql.wrapper_sql import WrapperOfTable

rawTable = WrapperOfTable("raw_expenses", db_config)
