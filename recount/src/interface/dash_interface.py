import numpy as np
import pandas as pd

from .default import *
from .default import deltaOfPeriod

__all__ = [
    "removeEmptyCategories",
    "getCategoriesOfDf",
    "getMainCategoriesOfDf",
    "getAlimentaryCategoriesOfDf",
    "dataframeToExpensesByColumn",
    "dataframeToSumExpensesByColumn",
    "dataframeToSumExpensesByPeriodAndColumn",
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


def getAlimentaryCategoriesOfDf(df: pd.DataFrame) -> pd.DataFrame:
    alimentary_df = df[ExpenseColumn.CATEGORY.value].apply(
        lambda x: x.split(":")[1]
        if len(x.split(":")) > 1 and x.split(":")[0] == "alimentary"
        else None
    )
    return alimentary_df


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


def dataframeToSumExpensesByPeriodAndColumn(
    df: pd.DataFrame, column: str, period: str
) -> list:
    min_date = minDateOfDataframe(df)
    max_date = maxDateOfDataframe(df)
    delta_period = deltaOfPeriod(period)

    expenses_by_period_and_category = {}

    while max_date > min_date:
        period_df = dataframeOfPeriod(df, min_date, delta_period)
        unique_categories = [
            category
            for category in period_df[column].unique()
            if not pd.isnull(category)  # case pd.null ?
        ]
        sum_expenses = {
            i: dict(
                x=[min_date],
                y=[
                    np.sum(
                        period_df[period_df[column] == i][ExpenseColumn.AMOUNT.value]
                    )
                ],
                name=i,
            )
            for i in unique_categories
        }
        updateDictAUsingDictB(expenses_by_period_and_category, sum_expenses)
        min_date += delta_period
    # list_dict_expenses = list(expenses_by_period_and_category.values())
    # list_dict_expenses.sort(key=sortByName, reverse=True)
    list_expenses_by_period_and_category = list(
        expenses_by_period_and_category.values()
    )
    return list_expenses_by_period_and_category
