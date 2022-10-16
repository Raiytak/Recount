# -*- coding: utf-8 -*-
import unidecode

import numpy as np
import pandas as pd


class ReviewerDataframe:
    def __init__(self, TSTAuthorized):
        self._tst_json = TSTAuthorized.getJson()

    def checkConformity(self, dataframe):
        self.checkThemesAndSubthemes(dataframe)

    def checkThemesAndSubthemes(self, dataframe):
        def chekTSTByRow(row):
            category = row["Category"]
            if (category == str(np.nan)) or (category == "reimbursement"):
                return row
            if category in self._tst_json.keys():
                theme = row["Theme"]
                if (theme in self._tst_json[category]) or (theme == str(np.nan)):
                    return row
                self.printSubthemeError(row)
                print("Error of THEME in row :\n", row)
                # raise Exception
            self.printThemeError(row)
            print("Error of CATEGORY in row :\n", row)
            # raise Exception

        dataframe.apply(chekTSTByRow, axis=1)

    def printSubthemeError(self, row):
        print("ERROR THEME :")
        print("In row ", row["ID"], "orthograph error in theme : ", row["Theme"])

    def printThemeError(self, row):
        print("ERROR CATEGORY :")
        print("In row ", row["ID"], "orthograph error in category : ", row["Category"])
