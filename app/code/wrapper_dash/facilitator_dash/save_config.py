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
        return self.AccessNotebookExcelConfig.updateJson(config_json)