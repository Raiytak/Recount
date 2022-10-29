import numpy as np
import pandas as pd

from .default import *

__all__ = [
    "removeEmptyCategories",
    "getCategoriesOfDf",
    "getMainCategoriesOfDf",
    "dataframeToExpensesByColumn",
    "dataframeToSumExpensesByColumn",
]


def removeEmptyCategories(df: pd.DataFrame) -> None:
    df.dropna(subset=[ExpenseColumn.CATEGORY.value], inplace=True)


def getCategoriesOfDf(df: pd.DataFrame) -> pd.DataFrame:
    categories = df[ExpenseColumn.CATEGORY.value]
    return categories


def getMainCategoriesOfDf(df: pd.DataFrame) -> pd.DataFrame:
    """Return the first/main category of each expense"""
    main_categories = df[ExpenseColumn.CATEGORY.value].apply(lambda x: x.split(":")[0])
    return main_categories


def dataframeToExpensesByColumn(df: pd.DataFrame, column: str) -> list:
    def sortByName(dict_named):
        return dict_named["name"]

    themes = [val for val in df[column].unique()]  # case pd.null ?
    expenses = [
        dict(
            x=df[df[column] == i][ExpenseColumn.DATE.value],
            y=df[df[column] == i][ExpenseColumn.AMOUNT.value],
            text=df[df[column] == i][ExpenseColumn.DESCRIPTION.value],
            name=i,  # useful to sort
        )
        for i in themes
    ]
    expenses.sort(key=sortByName)
    return expenses


def dataframeToSumExpensesByColumn(df: pd.DataFrame, column: str) -> dict:
    expenses = {"values": [], "names": [], "labels": []}
    themes = [val for val in df[column].unique()]  # case pd.null ?
    themes.sort()
    for i in themes:
        expenses["values"].append(np.sum(df[df[column] == i]["amount"]))
        expenses["names"].append(i)
        expenses["labels"].append(i)
    return expenses
