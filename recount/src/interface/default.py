from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

__all__ = [
    "ExpenseColumn",
    "EXPENSE_COLUMNS",
    "EXCEL_COLUMNS",
    "DEFAULT_DATE_FORMAT",
    "dateToString",
    "addDeltaToDatetime",
    "minDateOfDataframe",
    "maxDateOfDataframe",
    "dataframeOfPeriod",
    "updateDictAUsingDictB",
]


class ExpenseColumn(Enum):
    """Default columns"""

    ID = "id"
    USERNAME = "username"
    DATE = "date"
    AMOUNT = "amount"
    CURRENCY = "currency"
    CATEGORY = "category"
    RECEIVER = "receiver"
    PLACE = "place"
    DESCRIPTION = "description"
    PAYEMENT_METHOD = "payment_method"


EXPENSE_COLUMNS = [col.value for col in ExpenseColumn]
EXCEL_COLUMNS = [col.value for col in ExpenseColumn if col != ExpenseColumn.USERNAME]

DEFAULT_DATE_FORMAT = "%Y-%m-%d"


def dateToString(date: datetime) -> str:
    return date.strftime(DEFAULT_DATE_FORMAT)


class Period:
    WEEK = "week"
    MONTH = "month"
    QUARTER = "semester"
    ANNUAL = "annual"


class Frequence(Enum):
    WEEK = "W"
    MONTH = "M"
    QUARTER = "3M"
    ANNUAL = "Y"


def addDeltaToDatetime(start_date: datetime, period: str) -> datetime:
    delta = deltaOfPeriod(period)
    end_date = start_date + delta
    return end_date


def deltaOfPeriod(period: str) -> datetime:
    if period == Period.WEEK:
        delta = relativedelta(weeks=1)
    # The substraction of one day prevents the graphs from including one day in two periods
    elif period == Period.MONTH:
        delta = relativedelta(months=1) - relativedelta(days=1)
    elif period == Period.QUARTER:
        delta = relativedelta(months=4) - relativedelta(days=1)
    elif period == Period.ANNUAL:
        delta = relativedelta(years=1) - relativedelta(days=1)
    else:
        raise AttributeError(
            "Period not accepted :{}\nonly 'week', 'month', 'quarter'  and 'year' are authorized".format(
                period
            )
        )
    return delta


def minDateOfDataframe(df: pd.DataFrame) -> str:
    return df[ExpenseColumn.DATE.value].min()


def maxDateOfDataframe(df: pd.DataFrame) -> str:
    return df[ExpenseColumn.DATE.value].max()


def dataframeOfPeriod(
    df: pd.DataFrame, start_date: datetime, delta_period: relativedelta
) -> pd.DataFrame:
    """start_date >= DF <= start_date + perdiod"""
    date_column = ExpenseColumn.DATE.value
    end_date = start_date + delta_period
    after_start = df[date_column] >= start_date
    before_end = df[date_column] <= end_date
    return df.loc[after_start & before_end]


# def groupByColumnAndSumByFrequence(df: pd.DataFrame, freq: Frequence):
#     df_grouped = df.groupby(
#         ["Name", pd.Grouper(key=ExpenseColumn.DATE.value, freq=freq.value)]
#     )["Quantity"]
#     df_sum = df_grouped.sum()
#     df_reset = df_sum.reset_index()
#     df_sorted = df_reset.sort_values("Date")
#     return df_sorted


def updateDictAUsingDictB(dictA: dict, dictB: dict) -> dict:
    for key, value in dictB.items():
        if key not in dictA.keys():
            dictA[key] = value
        else:
            for subkey, subvalue in value.items():
                if type(subvalue) == list:
                    dictA[key][subkey] += subvalue
    return dictA
