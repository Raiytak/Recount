# -*- coding: utf-8 -*-
import unidecode

import numpy as np
import pandas as pd


class ReviewerDataframe():
    def __init__(self, TSTAuthorized):
        self._tst_json = TSTAuthorized.getJson()   
        
        
    def checkConformity(self, dataframe):
        self.checkThemesAndSubthemes(dataframe)
        
    
    def checkThemesAndSubthemes(self, dataframe):
        def chekTSTByRow(row):
            theme = row["Theme"]
            if (theme == str(np.nan)) or (theme == "remboursement"):
                return row
            if (theme in self._tst_json.keys()):
                subtheme = row["Soustheme"]
                if (subtheme in self._tst_json[theme]) or (subtheme == str(np.nan)):
                    return row
                self.printSubthemeError(row)
                print("Error of SUBTHEME in row :\n", row)
                # raise Exception
            self.printThemeError(row)
            print("Error of THEME in row :\n", row)
            # raise Exception
        dataframe.apply(chekTSTByRow, axis=1)
    

    def printSubthemeError(self, row):
        print("ERROR SUBTHEME :")
        print("In row ", row["ID"], "orthograph error in subtheme : ", row["Soustheme"])

    def printThemeError(self, row):
        print("ERROR THEME :")
        print("In row ", row["ID"], "orthograph error in theme : ", row["Theme"])
