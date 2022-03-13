# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Convert dataframe to a list of dict, which are the data used by
the Dash graphs.
"""

import numpy as np

from .date import dateDelta


def convertDataframeToGraphDataForEachUniqValueInColumn(
    dataframe, column_name: str
) -> list:
    df = dataframe
    unique_theme = [val for val in df[column_name].unique() if val is not None]
    unique_theme.sort()
    list_dict_expenses = [
        dict(
            x=df[df[column_name] == i]["date"].values,
            y=df[df[column_name] == i]["amount"].values,
            text=df[df[column_name] == i]["description"].values,
            name=i,
        )
        for i in unique_theme
    ]
    # list_dict_expenses.sort(key=sortByName)
    return list_dict_expenses


def convertDataframeToSumDataForEachUniqValueInColumn(
    dataframe, column_name: str
) -> dict:
    df = dataframe
    dict_expenses = {"values": [], "names": [], "labels": []}
    unique_theme = [val for val in df[column_name].unique() if val is not None]
    unique_theme.sort()
    for i in unique_theme:
        dict_expenses["values"].append(np.sum(df[df[column_name] == i]["amount"]))
        dict_expenses["names"].append(i)
        dict_expenses["labels"].append(i)
    return dict_expenses


def converDataframeToDataGroupedByDateDeltaAndColumn(
    dataframe, column_name: str, period: str = "week"
):
    dict_returned = {}
    dates = dataframe["date"]
    max_date = dates.max()
    curr_date = dates.min()

    while curr_date <= max_date:
        next_date = dateDelta(curr_date, period)
        data = dataframe[(dates < next_date) & (dates >= curr_date)]
        unique_theme = [val for val in data[column_name].unique() if val is not None]
        dict_expenses = {
            i: dict(
                x=[curr_date],
                y=[np.sum(data[data[column_name] == i]["amount"])],
                name=i,
            )
            for i in unique_theme
        }
        updateDictWithLists(dict_returned, dict_expenses)
        curr_date = next_date
    expenses = list(dict_returned.values())
    expenses.sort(key=sortByName, reverse=True)
    return expenses


def updateDictWithLists(dictA, dictB):
    for key, value in dictB.items():
        if key not in dictA.keys():
            dictA[key] = value
        else:
            for subkey, subvalue in value.items():
                if type(subvalue) == list:
                    dictA[key][subkey] += subvalue
    return dictA


def sortByName(dict_named):
    return dict_named["name"]
