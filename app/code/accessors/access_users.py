import json

from accessors import path_files


class AccessUsers:
    def __init__(self):
        self.ApplicationDataPath = path_files.ApplicationDataPath()
        self.PathInformation = self.ApplicationDataPath.PathInformation

    def getUsersPath(self):
        self.PathInformation.folders = [self.ApplicationDataPath.folder_config]
        self.PathInformation.filename = "users.json"
        return self.ApplicationDataPath.formPathUsing(self.PathInformation)

    def getUsers(self):
        path_users = self.getUsersPath()
        with open(path_users, "r") as json_file:
            data = json.load(json_file)
        return data
