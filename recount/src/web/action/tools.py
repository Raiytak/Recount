import dash
from datetime import datetime
from dateutil.relativedelta import relativedelta

from src.security.authentification import getUsername

__all__ = ["getUsername", "getIdButtonClicked", "deltaToDatetime"]


def getIdButtonClicked():
    return [p["prop_id"] for p in dash.callback_context.triggered][0]


def deltaToDatetime(start_date: datetime, period: str) -> datetime:
    """Returns the current date with the desired period added to it"""
    if period == "week":
        end_date = start_date + relativedelta(weeks=1)
    # The substraction of one day prevents the graphs from taking an extra day
    elif period == "month":
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
    elif period == "semestre":
        end_date = start_date + relativedelta(months=4) - relativedelta(days=1)
    elif period == "annual":
        end_date = start_date + relativedelta(years=1) - relativedelta(days=1)
    else:
        raise AttributeError(
            "Period not accepted :{}\nonly 'week', 'month', 'semestre'  and 'year' are authorized".format(
                period
            )
        )
    return end_date
