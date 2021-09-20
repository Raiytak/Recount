# import time

# from accessors.access_config import AccessConfig
# from wrapper_sql.wrapper_sql import WrapperOfTable

# myAccessConfig = AccessConfig()


# # Test decrypted
# db_config = myAccessConfig.getDatabaseConfig()
# myRawTable = WrapperOfTable("raw_expenses", db_config)

# request_sql = ""
# start_time = time.monotonic()
# myRawTable.insert()
# end_time = time.monotonic()
# print("Duration : ", start_time - end_time)


# # Test encrypted
# db_config["db"] = "recount"
# myEncryptedRawTable = WrapperOfTable("raw_expenses", db_config)

# request_sql = ""
# start_time = time.monotonic()
# myEncryptedRawTable.insert()
# end_time = time.monotonic()
# print("Duration : ", start_time - end_time)
