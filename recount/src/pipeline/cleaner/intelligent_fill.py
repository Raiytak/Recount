# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This module parse the description column of the excel to get information about the company and the theme of each row.
To do so, the results are saved in the convert_descr_to_theme.json file in data.

Each time a combo of category, theme and description is founded, it is created in this file or the combo number is increased by one.
When there is only a description on the row, the module looks at the existing combos and returns the one that has the maximum combo number,
meaning that this is the most probable one.
"""

import numpy as np


# TODO 9169: rework of intelligent fill, improve robustness and logic


class IntelligentFill:
    def __init__(self, intelligent_fill):
        self.intelligent_fill = intelligent_fill

    def fillBlanks(self, dataframe):
        if self.intelligent_fill != {}:
            self.fillBlanksUsingCompany(dataframe)

    # TODO: Add only if category in user's authorized categories
    def fillBlanksUsingCompany(self, dataframe):
        def fillRowUsingEntreprise(row):
            if row["Category"] == str(np.nan):
                company = row["Company"]
                category = self.convertCompanyToCategory(company)
                row["Category"] = category
            return row

        dataframe = dataframe.apply(fillRowUsingEntreprise, axis=1)
        return dataframe

    def convertCompanyToCategory(self, company):
        best_category = str(np.nan)
        if company != str(np.nan):
            categories = self.intelligent_fill["Company"]
            if company in categories.keys():
                if categories[company] != {}:
                    best_category = max(categories, key=categories.get)
        return best_category


# TODO: Refactor this function
# TODO 1093 : Adapt intelligent fill update
# TODO: set the probability between 0 and 1, and count the number of occurence
# TODO: have some sort of coefficient that reduces the power of each user each time they use / add a cat + theme


class UpdateConversionJson:
    def __init__(self):
        self.AccessDescrToTheme = AccessDescrToTheme()
        self.intelligent_fill = self.AccessDescrToTheme.getJsonDescrToTheme()

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
        self.AccessDescrToTheme.updateDescrConvJson(self.intelligent_fill)

    def _updateConversionEntrepriseJson(self, company, c_t, value, type_output):
        # type_output = "c_t" or "Theme"
        if company != str(np.nan):
            try:
                self.intelligent_fill["Company"][company][type_output][c_t] += value
            except KeyError:
                try:
                    self.intelligent_fill["Company"][company][type_output][c_t] = value
                except KeyError:
                    try:
                        self.intelligent_fill["Company"][company][type_output] = {}
                        self.intelligent_fill["Company"][company][type_output][
                            c_t
                        ] = value
                    except KeyError:
                        try:
                            self.intelligent_fill["Company"][company] = {}
                            self.intelligent_fill["Company"][company][type_output] = {}
                            self.intelligent_fill["Company"][company][type_output][
                                c_t
                            ] = value
                        except KeyError:
                            self.intelligent_fill["Company"] = {}
                            self.intelligent_fill["Company"][company] = {}
                            self.intelligent_fill["Company"][company][type_output] = {}
                            self.intelligent_fill["Company"][company][type_output][
                                c_t
                            ] = value

    # def getListStopWords(self):
    #     en_stop_words = stop_words.get_stop_words("english")
    #     fr_stop_words = stop_words.get_stop_words("french")
    #     stop_words = en_stop_words + fr_stop_words
    #     return stop_words
