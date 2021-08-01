from decouple import config


class AccessConfig:
    def __init__(self):
        self.db_conf = ["host", "port", "db", "user", "password"]

    def getDatabaseConfig(self):
        db_conf_values = [config(key) for key in self.db_conf]
        database_config = {
            key: value for (key, value) in zip(self.db_conf, db_conf_values)
        }
        return database_config
