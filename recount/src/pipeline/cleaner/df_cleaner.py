# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Clean a dataframe to save it as the clean_excel 
"""
# TODO: change the currency logic

import unidecode

import numpy as np
import pandas as pd


def addDateEverywhere(dataframe):
    # TODO: improve this mechanism
    last_date = np.datetime64("2019-07-01")
    for i in range(len(dataframe)):
        current_date = dataframe.loc[i, "Date"]
        if pd.isnull(current_date):
            dataframe.at[i, "Date"] = last_date
        else:
            last_date = current_date


def convertDateToStr(dataframe):
    def convertDatetimeToSQLFormat(datetime_elem):
        time_sql_format = datetime_elem.strftime("%Y-%m-%d")
        return time_sql_format

    dataframe["Date"].apply(convertDatetimeToSQLFormat)


def removeLinesWithoutExpense(dataframe):
    for i in range(len(dataframe)):
        current_line = dataframe.loc[i]
        if pd.isnull(current_line["Expense Euros"]) and pd.isnull(
            current_line["Expense Dollars"]
        ):
            dataframe.drop(i, inplace=True)


def summarizeExpenses(dataframe):
    """Add all expenses into one expense in EUROS"""
    list_expenses = getListSummarizedExpenses(dataframe)
    dataframe.insert(loc=0, column="Expenses", value=list_expenses)


def getListSummarizedExpenses(dataframe):
    df_expenses = dataframe.loc[:, ["Expense Euros", "Expense Dollars"]]
    df_expenses = df_expenses.fillna(0)  # Fill the nan values with 0
    df_expenses = [convertExpenseInEuros(row) for index, row in df_expenses.iterrows()]
    return df_expenses


def convertExpenseInEuros(row):
    expenseE = row["Expense Euros"]
    expenseD = row["Expense Dollars"]
    return np.around(expenseE + (expenseD / 1.5), 2)  # Limit the number of digits to 2


# def removeRawExpensesColumns(dataframe):
#     dataframe.drop(columns=["Expense Euros", "Expense Dollars"])


def convertExpensesToStr(dataframe):
    dataframe["Expenses"] = dataframe["Expenses"].apply(str)


def removeUselessColumns(dataframe):
    # list_columns = ["Category", "Description", "Date",
    #                 "Expense Euros", "Expense Dollars", "Sum Euros", "Sum Dollars",
    #                 "Excess E", "Excess D"]
    list_columns = [
        "Expense Euros",
        "Expense Dollars",
        "Sum Euros",
        "Sum Dollars",
        "Excess E",
        "Excess D",
        "TemporaryDescription",
    ]
    for column_name in list_columns:
        try:
            dataframe.drop(columns=column_name, axis=1, inplace=True)
        except Exception as e:
            pass
    list_columns_df = dataframe.columns
    for column_name in list_columns_df:
        if "Unnamed" in column_name:
            dataframe.drop(columns=column_name, axis=1, inplace=True)


def normalizeDescription(dataframe):
    dataframe["Description"] = dataframe["Description"].apply(str)
    dataframe["Description"] = dataframe["Description"].apply(removeAccentAndLowerStr)


def splitAndCleanCategory(dataframe):
    def convertIntoCategory(category_theme):
        category_theme = str(category_theme)
        list_tst = category_theme.split(":")
        if list_tst != []:
            return list_tst[0]

    def convertIntoTheme(category_theme):
        category_theme = str(category_theme)
        list_tst = category_theme.split(":")
        if len(list_tst) > 1:
            return list_tst[1]
        return str(np.nan)

    dataframe["Theme"] = dataframe["Category"].apply(convertIntoTheme)
    dataframe["Category"] = dataframe["Category"].apply(convertIntoCategory)


def splitAndCleanDescription(dataframe):
    def isOnlyCompany(raw_description):
        splited_descr = raw_description.split()
        if len(splited_descr) > 1:
            return False
        resplited_descr = splited_descr[0].split(":")
        resplited_descr = removeSpaceInList(resplited_descr)
        if len(resplited_descr) > 1:
            return False
        return True

    def convertIntoCompany(raw_description):
        if isOnlyCompany(raw_description):
            return raw_description
        list_descr = raw_description.split(":")
        list_descr = removeSpaceInList(list_descr)
        if len(list_descr) > 1:
            entreprise = list_descr[0]
            if entreprise == "":
                return str(np.nan)
            return list_descr[0]
        return str(np.nan)

    def convertIntoDescription(raw_description):
        if isOnlyCompany(raw_description):
            return str(np.nan)
        list_descr = raw_description.split(":")
        if len(list_descr) > 1:
            return list_descr[1]
        return list_descr[0]

    dataframe["TemporaryDescription"] = dataframe["Description"]
    dataframe["Company"] = dataframe["TemporaryDescription"].apply(convertIntoCompany)
    dataframe["Description"] = dataframe["TemporaryDescription"].apply(
        convertIntoDescription
    )


def removeAllApostrophes(dataframe):
    list_to_normalize = ["Company", "Description"]
    for column in list_to_normalize:
        dataframe[column] = dataframe[column].apply(removeApostrophe)


def removeAccentAndLowerStr(text):
    text = unidecode.unidecode(text)  # Remove accents
    text = text.lower()
    return text


def removeApostrophe(text):
    # Have to remove the apostrophes because that pymysql doesn't support it
    text = text.replace("'", " ")
    return text


def removeSpaceInList(list_text):
    list_ret = []
    for text in list_text:
        if text != "":
            first_text = text
            if text[0] == " ":
                first_text = first_text[1:]
            second_text = first_text
            if text[-1] == " ":
                second_text = second_text[:-1]
            list_ret.append(second_text)
    return list_ret


def convertStrNanToNan(dataframe):
    dataframe.replace("nan", np.NaN, inplace=True)
