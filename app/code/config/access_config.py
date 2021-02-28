import getpass
import json



# Dict that initialises the config.json by replacing the right values
DICT_PATHS = {
    "manual_deployment_linux":{
        "USERNAME":getpass.getuser(),
        "USER_HOME":"/home",
        "MAIN_FOLDER":"/Desktop/Projets/Comptes",
        "PATH_TO_MAIN_FOLDER":"/home"+"/"+getpass.getuser()+"/Desktop/Projets/Comptes"
    },
    "manual_deployment_linux_using_docker_version":{
        "USERNAME":getpass.getuser(),
        "USER_HOME":"/home",
        "MAIN_FOLDER":"/Desktop/Projets/Comptes",
        "PATH_TO_MAIN_FOLDER":"/home"+"/"+getpass.getuser()+"/Desktop/Projets/Comptes/app"
    },
    "docker_deployment_linux":{
        "USERNAME":"",
        "USER_HOME":"",
        "PATH_TO_MAIN_FOLDER":"",
        "PATH_TO_MAIN_FOLDER":""
    }
}

DICT_CONNEXION_MYSQL = {
    "manual_deployment_linux":{
        "host":"localhost",
        "db":"expenses",
        "user":"myuser",
        "passwd":"mypass"
    },
    "manual_deployment_linux_using_docker_version":{
        "host":"localhost",
        "db":"expenses",
        "user":"myuser",
        "passwd":"mypass"
    },
    "docker_deployment_linux":{
        "host":"",
        "db":"expenses",
        "user":"myuser",
        "passwd":"mypass"
    }
}




class AccessConfig():
    def __init__(self):
        # ===== LINE TO COMMENT TO STOP THE AUTOMATIC UPDATE OF THE config.json FILE =====
        self.updateTheConfigFile()

    def dictPathsByDeploymentMethod(self):
        relative_path_to_config = "/code/config/config.json"
        path_to_main_folder = DICT_PATHS["manual_deployment_linux"]["PATH_TO_MAIN_FOLDER"]

        manual_deployment_linux__path_to_config_file = path_to_main_folder + relative_path_to_config

        # Path for the docker Deployment on linux
        docker_deployment_linux__path_to_config_file = relative_path_to_config

        # Path for the docker Deployment on linux TEST
        path_to_main_folder = DICT_PATHS["manual_deployment_linux_using_docker_version"]["PATH_TO_MAIN_FOLDER"]
        manual_deployment_linux_using_docker_version__path_to_config_file = path_to_main_folder + relative_path_to_config

        dict_paths = {"manual_deployment_linux":manual_deployment_linux__path_to_config_file,
                       "docker_deployment_linux":docker_deployment_linux__path_to_config_file,
                       "manual_deployment_linux_using_docker_version":manual_deployment_linux_using_docker_version__path_to_config_file} 
        return dict_paths


    def findTheDeploymentMethodUsingPathOpeningTries(self):
        for key,value in self.dictPathsByDeploymentMethod().items():
            try:
                with open(value, "r") as json_file:
                    return key
            except FileNotFoundError:
                pass

    # This method permits to update the USERNAME and USER_HOME in the config file depending on the deployment method founded
    def updatePathsOfTheConfigFile(self, data, deployment_method):
        for element in data["paths"]:
            data["paths"][element] = DICT_PATHS[deployment_method][element]
        self.writeConfig(data)

    # This method permits to update the connexion to MYSQL in the config file depending on the deployment method founded
    def updateMysqlConfOfTheConfigFile(self, data, deployment_method):
        for element in data["mysql"]:
            data["mysql"][element] = DICT_CONNEXION_MYSQL[deployment_method][element]
        self.writeConfig(data)

    # Update the config.json file depending on the deployment method founded
    def updateTheConfigFile(self):
        deployment_method = self.findTheDeploymentMethodUsingPathOpeningTries()
        data = self.getConfig()
        self.updatePathsOfTheConfigFile(data, deployment_method)
        self.updateMysqlConfOfTheConfigFile(data, deployment_method)

    def getConfigPath(self):
        dict_paths = self.dictPathsByDeploymentMethod()
        key = self.findTheDeploymentMethodUsingPathOpeningTries()
        return dict_paths[key]

    def getConfig(self):
        config_path = self.getConfigPath()
        with open(config_path, "r") as json_file:
            data = json.load(json_file)
        return data

    def writeConfig(self, data):
        config_path = self.getConfigPath()
        with open(config_path, "w") as json_file:
            json.dump(data, json_file)



# myAccessConfig = AccessConfig()
# print(myAccessConfig.getConfig())