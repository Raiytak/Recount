# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import stop_words



class IntelligentFill():
    def __init__(self, AccessDescrToTheme):
        self._descr_to_theme_json = AccessDescrToTheme.getJsonDescrToTheme()      
    
    def intelligentFillBlankThemeUsingEntreprise(self, dataframe):
        if self._descr_to_theme_json != {}:
            dataframe = self.fillBlanksUsingEntreprise(dataframe)
            # dataframe = self.fillBlanksUsingDescription(dataframe) #TODO
        return dataframe
        
    def fillBlanksUsingEntreprise(self, dataframe):
        def fillRowUsingEntreprise(row):
            if row["Theme"] == str(np.nan):
                entreprise = row["Entreprise"]
                theme = self.convertEntrepriseToThemeSubtheme(entreprise, "Theme")
                row["Theme"] = theme
            if row["Soustheme"] == str(np.nan):
                entreprise = row["Entreprise"]
                soustheme = self.convertEntrepriseToThemeSubtheme(entreprise, "Soustheme")
                row["Soustheme"] = soustheme
            return row
        dataframe = dataframe.apply(fillRowUsingEntreprise, axis=1)
        return dataframe
    
    def convertEntrepriseToThemeSubtheme(self, entreprise, t_st):
        conv_json = self._descr_to_theme_json
        best_theme = str(np.nan)
        if entreprise != str(np.nan):
            try:
                themes_json = conv_json["Entreprise"][entreprise][t_st]
                if str(np.nan) in themes_json.keys():
                    del themes_json[str(np.nan)]
                if themes_json != {}:
                    best_theme = max(themes_json, key=themes_json.get)
            except KeyError:
                pass #Means that there is no information for this entreprise
        return best_theme



class UpdateConversionJson():
    def __init__(self, AccessDescrToTheme):
        self.AccessDescrToTheme = AccessDescrToTheme
        self._descr_to_theme_json = AccessDescrToTheme.getJsonDescrToTheme()
    
    def updateConversionJsonUsingDataframe(self, dataframe):
        list_tst = ["Theme", "Soustheme"]
        # list_entre_descr = ["Entreprise", "Description"]
        entreprise = "Entreprise"
        for TorST in list_tst:
            data = dataframe.groupby(TorST)[entreprise].value_counts()
            list_index = list(data.index)
            for index in list_index:
                theme_or_subtheme = index[0]
                entr_or_descr = index[1]
                value = int(data[index])
                self._updateConversionEntrepriseJson(entr_or_descr, theme_or_subtheme, value, TorST)
        self.AccessDescrToTheme.updateDescrConvJson(self._descr_to_theme_json)
        
    
    def _updateConversionEntrepriseJson(self, entreprise, t_st, value, type_output):
        #type_output = "t_st" or "Soustheme"
        if entreprise != str(np.nan):
            try:
                self._descr_to_theme_json["Entreprise"][entreprise][type_output][t_st] += value
            except KeyError:
                try:
                    self._descr_to_theme_json["Entreprise"][entreprise][type_output][t_st] = value
                except KeyError:
                    try:
                        self._descr_to_theme_json["Entreprise"][entreprise][type_output] = {}
                        self._descr_to_theme_json["Entreprise"][entreprise][type_output][t_st] = value
                    except KeyError:
                        try:
                            self._descr_to_theme_json["Entreprise"][entreprise] = {}
                            self._descr_to_theme_json["Entreprise"][entreprise][type_output] = {}
                            self._descr_to_theme_json["Entreprise"][entreprise][type_output][t_st] = value
                        except KeyError:
                            self._descr_to_theme_json["Entreprise"] = {}
                            self._descr_to_theme_json["Entreprise"][entreprise] = {}
                            self._descr_to_theme_json["Entreprise"][entreprise][type_output] = {}
                            self._descr_to_theme_json["Entreprise"][entreprise][type_output][t_st] = value
        
        
    # def getListStopWords(self):
    #     en_stop_words = stop_words.get_stop_words("english")
    #     fr_stop_words = stop_words.get_stop_words("french")
    #     stop_words = en_stop_words + fr_stop_words
    #     return stop_words
    
