import getpass
import json



class AccessUsers():
    def __init__(self, config_json):
        self.config_json = config_json
        self.relative_path_users = "/code/config/users.json"

    def getUsersPath(self):
        config = self.config_json
        main_path = config["paths"]["PATH_TO_MAIN_FOLDER"]
        users_path = main_path+self.relative_path_users
        return users_path
        

    def getUsers(self):
        users_path = self.getUsersPath()
        with open(users_path, "r") as json_file:
            data = json.load(json_file)
        return data
