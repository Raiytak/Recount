# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Clean a dataframe to save it as the clean_excel 
"""
# TODO: change the currency logic

import unidecode
import numpy as np
import pandas as pd
from datetime import date
from currency_converter import CurrencyConverter

from access import ConfigAccess

# TODO 2223 : Adapt cleaner df to custom user name column

__all__ = ["CleanerDataframe"]
"""Authorized currencies: 
[
    "AUD",
    "BGN",
    "BRL",
    "CAD",
    "CHF",
    "CNY",
    "CYP",
    "CZK",
    "DKK",
    "EEK",
    "EUR",
    "GBP",
    "HKD",
    "HRK",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "ISK",
    "JPY",
    "KRW",
    "LTL",
    "LVL",
    "MTL",
    "MXN",
    "MYR",
    "NOK",
    "NZD",
    "PHP",
    "PLN",
    "ROL",
    "RON",
    "RUB",
    "SEK",
    "SGD",
    "SIT",
    "SKK",
    "THB",
    "TRL",
    "TRY",
    "USD",
    "ZAR",
]"""


class CleanerDataframe:
    def __init__(self, equivalent_columns):
        self.equivalent_columns = equivalent_columns

    @property
    def amount(self):
        return self.equivalent_columns["amount"]

    @property
    def date(self):
        return self.equivalent_columns["date"]

    @property
    def currency(self):
        return self.equivalent_columns["currency"]

    @property
    def description(self):
        return self.equivalent_columns["description"]

    @property
    def description(self):
        return self.equivalent_columns["description"]

    @property
    def company(self):
        return self.equivalent_columns["company"]

    def replaceEmptyRowWithAboveValue(self, dataframe, column: str):
        last_value = dataframe.loc[0, column]
        for i in range(1, len(dataframe)):
            current_value = dataframe.loc[i, column]
            if pd.isnull(current_value):
                dataframe.at[i, column] = last_value
            else:
                last_value = current_value

    def addDateEverywhere(self, dataframe):
        self.replaceEmptyRowWithAboveValue(dataframe, self.date)

    def addCurrencyEverywhere(self, dataframe):
        self.replaceEmptyRowWithAboveValue(dataframe, self.currency)

    def removeLinesWithoutAmount(self, dataframe):
        for i in range(len(dataframe)):
            current_line = dataframe.loc[i]
            if pd.isnull(current_line[self.amount]):
                dataframe.drop(i, inplace=True)

    # TODO 5647 : Accelerate function,
    def convertAmountWithCurrencyAndDateIntoEuro(self, dataframe):
        def convertAmountCurrencyDateToEuro(row):
            converter = CurrencyConverter(
                str(ConfigAccess.currencies_rates_path),
                fallback_on_wrong_date=True,
                fallback_on_missing_rate=True,
                fallback_on_missing_rate_method="last_known",
            )
            converted_amount = converter.convert(
                row[self.amount], row[self.currency], "EUR", date=row[self.date],
            )
            return round(converted_amount, 2)

        dataframe[self.amount] = dataframe.loc[
            :, [self.amount, self.currency, self.date]
        ].apply(convertAmountCurrencyDateToEuro, axis=1)

    def convertAmountToStr(self, dataframe):
        dataframe[self.amount] = dataframe[self.amount].apply(str)

    def normalizeImportantColumns(self, dataframe):
        dataframe.rename(
            columns={
                value: key
                for key, value in self.equivalent_columns.items()
                if value != self.currency
            },
            inplace=True,
        )

    def removeUselessColumns(self, dataframe):
        list_columns = [
            column
            for column in dataframe.columns
            if not column in self.equivalent_columns.keys()
        ]
        dataframe.drop(columns=list_columns, axis=1, inplace=True)

    def normalizeDescription(self, dataframe):
        dataframe[self.description] = dataframe[self.description].apply(str)
        dataframe[self.description] = dataframe[self.description].apply(
            self.removeAccentAndLowerStr
        )

    def normalizeCompany(self, dataframe):
        dataframe[self.company] = dataframe[self.company].apply(str)
        dataframe[self.company] = dataframe[self.company].apply(
            self.removeAccentAndLowerStr
        )

    # TODO: Improve robustness of split and clean (use regex too)
    def splitAndCleanDescription(self, dataframe):
        def isOnlyCompany(raw_description):
            splited_descr = raw_description.split()
            if len(splited_descr) > 1:
                return False
            resplited_descr = splited_descr[0].split(":")
            resplited_descr = self.removeSpaceInList(resplited_descr)
            if len(resplited_descr) > 1:
                return False
            return True

        def converDescriptiontIntoCompany(raw_description):
            if isOnlyCompany(raw_description):
                return raw_description
            list_descr = raw_description.split(":")
            list_descr = self.removeSpaceInList(list_descr)
            if len(list_descr) > 1:
                entreprise = list_descr[0]
                if len(entreprise) == 0:
                    return str(np.nan)
                else:
                    if entreprise[0] == " ":
                        entreprise = entreprise[1:]
                    if entreprise[-1] == " ":
                        entreprise = entreprise[:-1]
                    return entreprise
            return str(np.nan)

        def removeCompanyFromDescription(raw_description):
            if isOnlyCompany(raw_description):
                return str(np.nan)
            list_descr = raw_description.split(":")
            if len(list_descr) > 1:
                if (len(list_descr[1]) > 1) and (list_descr[1][0] == " "):
                    return list_descr[1][1:]
                return list_descr[1]
            return list_descr[0]

        dataframe[self.company] = dataframe[self.description].apply(
            converDescriptiontIntoCompany
        )
        dataframe[self.description] = dataframe[self.description].apply(
            removeCompanyFromDescription
        )

    def removeAccentAndLowerStr(self, text):
        text = unidecode.unidecode(text)  # Remove accents
        text = text.lower()
        return text

    def removeApostrophe(self, text):
        """Have to remove the apostrophes because that pymysql doesn't support it"""
        if type(text) is str:
            text = text.replace("'", " ")
        return text

    # TODO: improve
    def removeSpaceInList(self, list_text):
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

    def convertStrNanToNan(self, dataframe):
        dataframe.replace("nan", np.NaN, inplace=True)
