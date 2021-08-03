import json

from accessors.path_files import UsersConfigPath


class AccessUsers:
    def __init__(self):
        self.UsersConfigPath = UsersConfigPath()
        self.PathInformation = self.UsersConfigPath.PathInformation

    def getUsers(self):
        path_users = self.UsersConfigPath.getUsersPath()
        with open(path_users, "r") as json_file:
            data = json.load(json_file)
        return data
