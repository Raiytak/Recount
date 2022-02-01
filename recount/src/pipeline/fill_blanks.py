# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This module parse the description column of the excel to get information about the company and the theme of each row.
To do so, the results are saved in the convert_descr_to_theme.json file in data.

Each time a combo of category, theme and description is founded, it is created in this file or the combo number is increased by one.
When there is only a description on the row, the module looks at the existing combos and returns the one that has the maximum combo number,
meaning that this is the most probable one.
"""

# TODO: make a convert_descr_to_theme.json file for each user and a global one
# TODO: set the probability between 0 and 1, and count the number of occurence
# TODO: have some sort of coefficient that reduces the power of each user each time they use / add a cat + theme

import numpy as np

from accessors.access_files import AccessDescrToTheme


class IntelligentFill:
    def __init__(self):
        self._descr_to_category_json = AccessDescrToTheme().getJsonDescrToTheme()

    def intelligentFillBlankCategoryUsingCompany(self, dataframe):
        if self._descr_to_category_json != {}:
            dataframe = self.fillBlanksUsingCompany(dataframe)
            # dataframe = self.fillBlanksUsingDescription(dataframe) #TODO
        return dataframe

    def fillBlanksUsingCompany(self, dataframe):
        def fillRowUsingEntreprise(row):
            if row["Category"] == str(np.nan):
                company = row["Company"]
                category = self.convertCompanyToCategoryAndTheme(company, "Category")
                row["Category"] = category
            if row["Theme"] == str(np.nan):
                company = row["Company"]
                theme = self.convertCompanyToCategoryAndTheme(company, "Theme")
                row["Theme"] = theme
            return row

        dataframe = dataframe.apply(fillRowUsingEntreprise, axis=1)
        return dataframe

    def convertCompanyToCategoryAndTheme(self, company, c_t):
        conv_json = self._descr_to_category_json
        best_theme = str(np.nan)
        if company != str(np.nan):
            try:
                themes_json = conv_json["Company"][company][c_t]
                if str(np.nan) in themes_json.keys():
                    del themes_json[str(np.nan)]
                if themes_json != {}:
                    best_theme = max(themes_json, key=themes_json.get)
            except KeyError:
                pass  # Means that there is no information for this company
        return best_theme


class UpdateConversionJson:
    def __init__(self):
        self.AccessDescrToTheme = AccessDescrToTheme()
        self._descr_to_category_json = self.AccessDescrToTheme.getJsonDescrToTheme()

    def updateConversionJsonUsingDataframe(self, dataframe):
        list_c_d = ["Company", "Description"]
        company = "Company"
        for cat_or_theme in list_c_d:
            data = dataframe.groupby(cat_or_theme)[company].value_counts()
            list_index = list(data.index)
            for index in list_index:
                theme_or_subtheme = index[0]
                entr_or_descr = index[1]
                value = int(data[index])
                self._updateConversionEntrepriseJson(
                    entr_or_descr, theme_or_subtheme, value, cat_or_theme
                )
        self.AccessDescrToTheme.updateDescrConvJson(self._descr_to_category_json)

    def _updateConversionEntrepriseJson(self, company, c_t, value, type_output):
        # type_output = "c_t" or "Theme"
        if company != str(np.nan):
            try:
                self._descr_to_category_json["Company"][company][type_output][
                    c_t
                ] += value
            except KeyError:
                try:
                    self._descr_to_category_json["Company"][company][type_output][
                        c_t
                    ] = value
                except KeyError:
                    try:
                        self._descr_to_category_json["Company"][company][
                            type_output
                        ] = {}
                        self._descr_to_category_json["Company"][company][type_output][
                            c_t
                        ] = value
                    except KeyError:
                        try:
                            self._descr_to_category_json["Company"][company] = {}
                            self._descr_to_category_json["Company"][company][
                                type_output
                            ] = {}
                            self._descr_to_category_json["Company"][company][
                                type_output
                            ][c_t] = value
                        except KeyError:
                            self._descr_to_category_json["Company"] = {}
                            self._descr_to_category_json["Company"][company] = {}
                            self._descr_to_category_json["Company"][company][
                                type_output
                            ] = {}
                            self._descr_to_category_json["Company"][company][
                                type_output
                            ][c_t] = value

    # def getListStopWords(self):
    #     en_stop_words = stop_words.get_stop_words("english")
    #     fr_stop_words = stop_words.get_stop_words("french")
    #     stop_words = en_stop_words + fr_stop_words
    #     return stop_words
