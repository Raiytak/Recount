import json

from accessors.path_files import ConfigPath


class AccessUsers:
    def __init__(self):
        self.ConfigPath = ConfigPath()
        self.PathInformation = self.ConfigPath.PathInformation

    def getUsers(self):
        path_users = self.ConfigPath.getUsersPath()
        with open(path_users, "r") as json_file:
            data = json.load(json_file)
        return data
