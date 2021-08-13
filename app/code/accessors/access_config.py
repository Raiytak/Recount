from decouple import config
from accessors.path_files import ConfigPath
import json


class AccessConfig:
    def __init__(self):
        self.ConfigPath = ConfigPath()
        self.db_conf = ["host", "port", "db", "user", "password"]

    def getDatabaseConfig(self):
        environment_type = self.determineEnvironmentType()
        global_configs = self.getGlobalConfigs()
        db_configs = global_configs[environment_type]["mysql"]
        dict_db_configs = {key: db_configs[key] for key in self.db_conf}
        return dict_db_configs

    def determineEnvironmentType(self):
        return config("environment")

    def getGlobalConfigs(self):
        path_global_configs = self.ConfigPath.getApplicationConfigsPath()
        with open(path_global_configs, "r") as json_file:
            data = json.load(json_file)
        return data

    def getSSLContext(self):
        cert_file = self.ConfigPath.getCertificatePath()
        private_key_file = self.ConfigPath.getPrivateKeyPath()
        return (cert_file, private_key_file)
