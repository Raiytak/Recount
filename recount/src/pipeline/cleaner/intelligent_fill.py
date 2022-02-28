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


def fillBlanks(dataframe, user_files):
    if user_files.intelligent_fill != {}:
        fillBlanksUsingCompany(dataframe, user_files)
        # fillBlanksUsingCompany(dataframe, intelligent_fill["Company"])


def fillBlanksUsingCompany(dataframe, user_files):
    def fillRowUsingCompany(row):
        if pd.isna(row["category"]):
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
            best_category = maxOfCategory("", intelligent_company[company])
    return best_category


def maxOfCategory(category_chain, curr_cat):
    if not curr_cat["c"]:
        return category_chain
    categories_entries = {key: curr_cat["c"][key]["ne"] for key in curr_cat["c"].keys()}
    best_category = max(categories_entries, key=categories_entries.get)
    category_chain += best_category
    return maxOfCategory(category_chain, curr_cat["c"][best_category])


# TODO: have some sort of coefficient that reduces the power of each user each time
# they use / add a cat + theme
# TODO: normalize to 1 the proportion
# TODO: Initialyze the intelligent fill example
# TODO: add unittest


def updateUserIntelligentFill(dataframe, user_files) -> dict:
    category_filter = dataframe["category"].notna()
    with_category = dataframe[category_filter]

    intelligent_fill = user_files.intelligent_fill.copy()

    for idx, row in with_category.iterrows():
        for column in ["company", "description"]:
            addCategoryForKeyInDict(
                intelligent_fill[column], row[column], row["category"],
            )
    user_files.updateIntelligentFill(intelligent_fill)


# TODO: make it work properly (issue on number entries)
def addCategoryForKeyInDict(intel_col: dict, key, category):
    def updateRecursivelyCategory(curr_intel, list_category):
        curr_cat = list_category.pop(0)

        if not curr_cat in curr_intel["c"].keys():
            curr_intel["c"][curr_cat] = {"ne": 1, "c": {}}
        else:
            curr_intel["c"][curr_cat]["ne"] += 1
        if list_category:
            updateRecursivelyCategory(curr_intel["c"][curr_cat], list_category)

    list_category = category.split(":")
    if pd.isna(key) or key == "nan":
        key = "_"
    if not key in intel_col.keys():
        intel_col[key] = {"ne": 0, "c": {}}
    intel_col[key]["ne"] += 1
    updateRecursivelyCategory(intel_col[key], list_category)

    # def getListStopWords(self):
    #     en_stop_words = stop_words.get_stop_words("english")
    #     fr_stop_words = stop_words.get_stop_words("french")
    #     stop_words = en_stop_words + fr_stop_words
    #     return stop_words
