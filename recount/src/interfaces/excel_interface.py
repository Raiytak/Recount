import pandas as pd


class ExcelColumns:
    """Default columns"""

    ID = "ID"
    USERNAME = "username"
    DATE = "date"
    AMOUNT = "amount"
    CURRENCY = "currency"
    CATEGORY = "category"
    RECEIVER = "receiver"
    PLACE = "place"
    DESCRITPION = "description"
    PAYEMENT_METHOD = "payment_method"


def dfFromData(data: bytes):
    dataframe = pd.read_excel(data)
    # TODO: add optional translations
    return dataframe

