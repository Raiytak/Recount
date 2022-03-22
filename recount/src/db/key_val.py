# import redis
# from typing import Union

# import sys
# from pathlib import Path


# def appPath():
#     root_path = Path().resolve()
#     if ".gitignore" not in [file_path.stem for file_path in root_path.iterdir()]:
#         if "__main__" not in [file_path.stem for file_path in root_path.iterdir()]:
#             raise FileNotFoundError(
#                 "Recount can only be launched where the .git folder is present or inside the recount folder"
#             )
#         else:
#             app_path = root_path
#     else:
#         app_path = root_path / "recount"
#     return app_path


# app_path = appPath()
# src_path = app_path / "src"
# sys.path.insert(0, str(app_path))
# sys.path.insert(0, str(src_path))


# from access import ConfigAccess


# class KeyValSocket:
#     def __init__(self, db_config: dict = None):
#         self.connection = self.createSocket(db_config)

#     def createSocket(self, db_config):
#         if db_config is None:
#             db_config = ConfigAccess.database_config_key_val
#         return redis.Redis(
#             host=db_config["host"],
#             port=db_config["port"],
#             db=0,
#             password=db_config["password"],
#         )

#     def __enter__(self):
#         return self.connection

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.connection.close()
#         del self


# class KeyValCache:
#     def __init__(self, db_config: dict = None):
#         self.db_config = db_config

#     def set(self, key: Union[bytes, str], value: Union[bytes, str, int, float]):
#         with KeyValSocket(self.db_config) as kv_socket:
#             kv_socket.set(key, value)


# db_config = ConfigAccess.database_config_key_val
# r = redis.Redis(
#     host=db_config["host"], port=db_config["port"], db=0, password=db_config["password"]
# )
# response = r.set("bar", {"foo": 1})
# print(response)
# response = r.get("foo")
# print(type(response))

