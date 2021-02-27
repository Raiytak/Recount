import os
import io
import base64
import csv
import pandas as pd

import update_db


class ConfigNotebookExcelSaver():
    def __init__(self, AccessNotebookExcelConfig):
        self.AccessNotebookExcelConfig = AccessNotebookExcelConfig


    def getConfig(self):
        return self.AccessNotebookExcelConfig.getJson()
    def updateConfig(self, data):
        return self.AccessNotebookExcelConfig.updateJson(data)


    def updateColumnsName(self, list_columns_name):
        config_json = self.getConfig()
        config_json["columns_name"] = {json_col_name["id"]:json_col_name["name"] for json_col_name in list_columns_name}
        return self.updateConfig(config_json)




class StandardButtonsConfigSaver():
    def __init__(self, AccessStandardButtonsConfig):
        self.AccessStandardButtonsConfig = AccessStandardButtonsConfig
        self._conf = self.getConfig()


    def getConfig(self):
        return self.AccessStandardButtonsConfig.getJson()
    def updateConfig(self, data):
        self.AccessStandardButtonsConfig.updateJson(data)


    def getOptionSavedOf(self, div_id, option_of_div):
        try:
            option_saved = self._conf[div_id][option_of_div]
            return option_saved
        except KeyError:
            return None

    # Used to save only value
    def saveListIdsListChildren(self, list_ids, list_children):
        for i in range(len(list_ids)):
            div_id = list_ids[i]
            div_option = list_children[i]
            self._conf[div_id] = {"value":div_option}
        self.updateConfig(self._conf)
