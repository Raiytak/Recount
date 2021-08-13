from decouple import config
from accessors.path_files import ConfigPath


class AccessConfig:
    def __init__(self):
        self.ConfigPath = ConfigPath()
        self.db_conf = ["host", "port", "db", "user", "password"]

    def getDatabaseConfig(self):
        db_conf_values = [config(key) for key in self.db_conf]
        database_config = {
            key: value for (key, value) in zip(self.db_conf, db_conf_values)
        }
        return database_config

    def getSSLContext(self):
        cert_file = self.ConfigPath.getCertificatePath()
        private_key_file = self.ConfigPath.getPrivateKeyPath()
        return (cert_file, private_key_file)
