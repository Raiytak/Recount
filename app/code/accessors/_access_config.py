import json
from decouple import config

from accessors import path_files


class AccessConfig:
    def __init__(self):
        self.ApplicationDataPath = path_files.ApplicationDataPath()
        self.PathInformation = self.ApplicationDataPath.PathInformation

    def getConfigPath(self):
        self.PathInformation.folders = [self.ApplicationDataPath.folder_config]
        self.PathInformation.filename = "database_configs.json"
        return self.ApplicationDataPath.formPathUsing(self.PathInformation)

    def getConfig(self):
        config_path = self.getConfigPath()
        with open(config_path, "r") as json_file:
            data = json.load(json_file)
        env_type = config("ENV_TYPE")
        return data[env_type]

    def writeConfig(self, data):
        config_path = self.getConfigPath()
        with open(config_path, "w") as json_file:
            json.dump(data, json_file)
