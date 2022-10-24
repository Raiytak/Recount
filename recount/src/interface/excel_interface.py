import pandas as pd
import io

__all__ = [
    "ExcelColumns",
    "dataToDf",
    "dfFromData",
]


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


def dataToDf(data: bytes):
    dataframe = pd.read_excel(data)
    # TODO: add optional translations
    return dataframe


def dfFromData(df: pd.DataFrame):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer)
        writer.save()
    buffer.seek(0)
    file_data = buffer.read()
    return file_data
