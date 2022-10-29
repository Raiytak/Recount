from enum import Enum
from datetime import datetime

__all__ = [
    "ExpenseColumn",
    "EXPENSE_COLUMNS",
    "EXCEL_COLUMNS",
    "DEFAULT_DATE_FORMAT",
    "dateToString",
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


def updateDictAUsingDictB(dictA: dict, dictB: dict) -> dict:
    for key, value in dictB.items():
        if key not in dictA.keys():
            dictA[key] = value
        else:
            for subkey, subvalue in value.items():
                if type(subvalue) == list:
                    dictA[key][subkey] += subvalue
    return dictA
