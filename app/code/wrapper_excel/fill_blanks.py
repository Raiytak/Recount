# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import stop_words



class IntelligentFill():
    def __init__(self, AccessDescrToTheme):
        self._descr_to_category_json = AccessDescrToTheme.getJsonDescrToTheme()      
    
    def intelligentFillBlankCategoryUsingEntreprise(self, dataframe):
        if self._descr_to_category_json != {}:
            dataframe = self.fillBlanksUsingEntreprise(dataframe)
            # dataframe = self.fillBlanksUsingDescription(dataframe) #TODO
        return dataframe
        
    def fillBlanksUsingEntreprise(self, dataframe):
        def fillRowUsingEntreprise(row):
            if row["Category"] == str(np.nan):
                company = row["Company"]
                theme = self.convertEntrepriseToThemeSubtheme(company, "Category")
                row["Category"] = theme
            if row["Theme"] == str(np.nan):
                company = row["Company"]
                soustheme = self.convertEntrepriseToThemeSubtheme(company, "Theme")
                row["Theme"] = soustheme
            return row
        dataframe = dataframe.apply(fillRowUsingEntreprise, axis=1)
        return dataframe
    
    def convertEntrepriseToThemeSubtheme(self, company, t_st):
        conv_json = self._descr_to_category_json
        best_theme = str(np.nan)
        if company != str(np.nan):
            try:
                themes_json = conv_json["Company"][company][t_st]
                if str(np.nan) in themes_json.keys():
                    del themes_json[str(np.nan)]
                if themes_json != {}:
                    best_theme = max(themes_json, key=themes_json.get)
            except KeyError:
                pass #Means that there is no information for this company
        return best_theme



class UpdateConversionJson():
    def __init__(self, AccessDescrToTheme):
        self.AccessDescrToTheme = AccessDescrToTheme
        self._descr_to_category_json = AccessDescrToTheme.getJsonDescrToTheme()
    
    def updateConversionJsonUsingDataframe(self, dataframe):
        list_c_d = ["Company", "Description"]
        # list_entre_descr = ["Entreprise", "Description"]
        company = "Company"
        for cat_or_theme in list_c_d:
            data = dataframe.groupby(cat_or_theme)[company].value_counts()
            list_index = list(data.index)
            for index in list_index:
                theme_or_subtheme = index[0]
                entr_or_descr = index[1]
                value = int(data[index])
                self._updateConversionEntrepriseJson(entr_or_descr, theme_or_subtheme, value, cat_or_theme)
        self.AccessDescrToTheme.updateDescrConvJson(self._descr_to_category_json)
        
    
    def _updateConversionEntrepriseJson(self, company, t_st, value, type_output):
        #type_output = "t_st" or "Theme"
        if company != str(np.nan):
            try:
                self._descr_to_category_json["Company"][company][type_output][t_st] += value
            except KeyError:
                try:
                    self._descr_to_category_json["Company"][company][type_output][t_st] = value
                except KeyError:
                    try:
                        self._descr_to_category_json["Company"][company][type_output] = {}
                        self._descr_to_category_json["Company"][company][type_output][t_st] = value
                    except KeyError:
                        try:
                            self._descr_to_category_json["Company"][company] = {}
                            self._descr_to_category_json["Company"][company][type_output] = {}
                            self._descr_to_category_json["Company"][company][type_output][t_st] = value
                        except KeyError:
                            self._descr_to_category_json["Company"] = {}
                            self._descr_to_category_json["Company"][company] = {}
                            self._descr_to_category_json["Company"][company][type_output] = {}
                            self._descr_to_category_json["Company"][company][type_output][t_st] = value
        
        
    # def getListStopWords(self):
    #     en_stop_words = stop_words.get_stop_words("english")
    #     fr_stop_words = stop_words.get_stop_words("french")
    #     stop_words = en_stop_words + fr_stop_words
    #     return stop_words
    
