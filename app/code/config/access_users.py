import getpass
import json

import os


class AccessUsers:
    def getUsersPath(self):
        path_file = os.path.abspath(__file__)
        users_path = path_file.replace("access_users.py", "users.json")
        return users_path

    def getUsers(self):
        users_path = self.getUsersPath()
        with open(users_path, "r") as json_file:
            data = json.load(json_file)
        return data
