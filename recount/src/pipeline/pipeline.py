"""
Prepare dataframe to be used for sql requests:
    - remove useless columns and lines
    - normalize columns name
    - normalize values
"""
# TODO: Next steps:
#     - reintroduce intelligent fill
#     - add possibilitity of translation
#     - reintroduce notion of reimbursement

import pandas as pd

from interface.default import ExpenseColumn
from .cleaner import *


@inplace
def cleanDf(df: pd.DataFrame, inplace: bool):
    # Modifications done inplace inside the function
    # but inplace variable is handled by the decorator
    inplace = True
    normalizeColumnsName(df, inplace)

    removeLinesWithEmptyColumn(df, ExpenseColumn.AMOUNT.value, inplace)

    replaceEmptyCellWithAboveCellForEachRow(df, ExpenseColumn.DATE.value, inplace)
    replaceEmptyCellWithAboveCellForEachRow(df, ExpenseColumn.CURRENCY.value, inplace)
    replaceEmptyCellWithAboveCellForEachRow(df, ExpenseColumn.PLACE.value, inplace)

    applyStrTo(df, ExpenseColumn.AMOUNT.value, inplace)
    applyStrTo(df, ExpenseColumn.DESCRIPTION.value, inplace)

    normalizeValuesOfColumns(df, ExpenseColumn.CATEGORY.value, inplace)
    normalizeValuesOfColumns(df, ExpenseColumn.DESCRIPTION.value, inplace)
    normalizeValuesOfColumns(df, ExpenseColumn.PLACE.value, inplace)
    normalizeValuesOfColumns(df, ExpenseColumn.PAYEMENT_METHOD.value, inplace)
    normalizeValuesOfColumns(df, ExpenseColumn.RECEIVER.value, inplace)
