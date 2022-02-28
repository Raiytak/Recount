# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This module parse the description column of the excel to get information about the company and the theme of each row.
To do so, the results are saved in the convert_descr_to_theme.json file in data.

Each time a combo of category, theme and description is founded, it is created in this file or the combo number is increased by one.
When there is only a description on the row, the module looks at the existing combos and returns the one that has the maximum combo number,
meaning that this is the most probable one.
"""

import pandas as pd
import numpy as np


# TODO 9169: rework of intelligent fill, improve robustness and logic


def fillBlanks(dataframe, user_files):
    if user_files.intelligent_fill != {}:
        fillBlanksUsingCompany(dataframe, user_files)
        # fillBlanksUsingCompany(dataframe, intelligent_fill["Company"])


def fillBlanksUsingCompany(dataframe, user_files):
    def fillRowUsingCompany(row):
        if pd.notna(row["category"]):
            category = convertCompanyToCategory(
                row["company"], user_files.intelligent_fill["company"]
            )
            row["category"] = category
        return row

    cleaned_dataframe = dataframe.apply(fillRowUsingCompany, axis=1)
    return cleaned_dataframe


def convertCompanyToCategory(company, intelligent_company):
    best_category = np.nan
    if pd.notna(company):
        if company in intelligent_company.keys():
            company_categories = intelligent_company[company]
            if company_categories != {}:
                best_category = max(company_categories, key=company_categories.get)
    return best_category


# TODO 1093 : Adapt intelligent fill update
# TODO: have some sort of coefficient that reduces the power of each user each time
# they use / add a cat + theme

# TODO: TEST
def updateUserIntelligentFill(dataframe, user_files) -> dict:
    category_filter = dataframe["category"].notna()
    with_category = dataframe[category_filter]

    intelligent_fill = user_files.intelligent_fill.copy()

    for idx, row in with_category.iterrows():
        for column in ["company", "description"]:
            addValueForKeyInDict(intelligent_fill, column, row[column], row["category"])
    user_files.updateIntelligentFill(intelligent_fill)


# TODO: make it work
def addValueForKeyInDict(intelligent_fill: dict, column, key, category):
    if pd.isna(key) or key == "nan":
        key = "_"
    intel_col = intelligent_fill[column]
    if not key in intel_col.keys():
        intel_col[key] = {}
        intelligent_fill["number entries"][key] = 0
    if intelligent_fill["number entries"][key] == 0:
        intel_col[key][category] = 1
        intelligent_fill["number entries"][key] = 1
        return
    last_tot = intelligent_fill["number entries"][key]
    intelligent_fill["number entries"][key] += 1
    tot = intelligent_fill["number entries"][key]
    proportion = last_tot / tot
    intel_col[key] = {k: val * proportion for k, val in intel_col[key].items()}
    if not category in intel_col[key].keys():
        intel_col[key][category] = proportion
    else:
        intel_col[key][category] += 1 - proportion

    # def getListStopWords(self):
    #     en_stop_words = stop_words.get_stop_words("english")
    #     fr_stop_words = stop_words.get_stop_words("french")
    #     stop_words = en_stop_words + fr_stop_words
    #     return stop_words
