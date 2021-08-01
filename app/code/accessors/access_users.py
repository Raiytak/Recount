import json
import os

class AccessUsers:
    def getUsersPath(self):
        path_users = os.environ["CODE_PATH"] + "/config/users.json"
        return path_users

    def getUsers(self):
        path_users = self.getUsersPath()
        with open(path_users, "r") as json_file:
            data = json.load(json_file)
        return data
