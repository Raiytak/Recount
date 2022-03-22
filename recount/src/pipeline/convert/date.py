# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Convert a date or a period given by the user into a dataframe.
The data comes from the user's data stored in MySQL.
"""
from typing import Union

import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from db.sql import UserSqlTable, SqlRequest, SqlKeyword


def convertDateToDataframe(
    start_date: str, end_date: str, user_table: UserSqlTable,
):
    request = convertDateToRequestSql(start_date, end_date, user_table)
    response = user_table.select(request)
    dataframe = translateSelectResponseToDataframe(response, user_table)
    dataframe = dataframe.set_index("ID")
    return dataframe


def convertDateToRequestSql(
    start_date: str, end_date: str, user_table: UserSqlTable,
) -> SqlRequest:
    condition = "date >= '" + start_date + "' AND date <= '" + end_date + "'"
    request = SqlRequest(
        SqlKeyword.SELECT, user_table.table_name, "*", condition, user_table.username,
    )
    return request


def getDatetime(my_date: Union[str, datetime.datetime]):
    if type(my_date) == datetime.datetime:
        return my_date
    try:
        formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S.%f")
        return formated_date
    except ValueError:
        pass
    try:
        formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S")
        return formated_date
    except ValueError:
        pass
    try:
        formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%d")
        return formated_date
    except ValueError:
        pass
    raise AttributeError("The provided str could not be parsed into a datetime")


def dateDelta(curr_date: datetime.datetime, period: str) -> datetime.datetime:
    """Returns the current date with the desired period added to it"""
    if period == "week":
        next_date = curr_date + relativedelta(weeks=1)
    # The substraction of one day prevents the graphs from taking an extra day
    elif period == "month":
        next_date = curr_date + relativedelta(months=1) - relativedelta(days=1)
    elif period == "semestre":
        next_date = curr_date + relativedelta(months=4) - relativedelta(days=1)
    elif period == "annual":
        next_date = curr_date + relativedelta(years=1) - relativedelta(days=1)
    else:
        raise AttributeError(
            "Period not accepted : \nonly 'week', 'month', 'semestre'  and 'year' are authorized"
        )
    return next_date


def convertPeriodToDate(
    start_date: Union[str, datetime.datetime], period: str
) -> datetime.datetime:
    start_date = getDatetime(start_date)
    end_date = dateDelta(start_date, period)
    return end_date


def translateSelectResponseToDataframe(response_sql, user_table):
    dataframe = pd.DataFrame(response_sql, columns=user_table.columns_name)
    return dataframe


def shapeDatetimeToSimpleDate(my_datetime):
    return my_datetime.strftime("%Y-%m-%d")
