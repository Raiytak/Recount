import json
import os

class AccessConfig:
    def getConfigPath(self):
        path_config = os.environ["CODE_PATH"] + "/config/config.json"
        return path_config

    def getConfig(self):
        config_path = self.getConfigPath()
        with open(config_path, "r") as json_file:
            data = json.load(json_file)
        return data

    def writeConfig(self, data):
        config_path = self.getConfigPath()
        with open(config_path, "w") as json_file:
            json.dump(data, json_file)
