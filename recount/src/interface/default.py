from enum import Enum


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
    DESCRITPION = "description"
    PAYEMENT_METHOD = "payment_method"


EXPENSE_COLUMNS = [col.value for col in ExpenseColumn]
EXCEL_COLUMNS = [col.value for col in ExpenseColumn if col != ExpenseColumn.USERNAME]
