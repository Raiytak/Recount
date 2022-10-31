import typing
import pandas as pd
import unidecode

from interface.default import EXCEL_COLUMNS


def inplace(func):
    def inner(*args, **kwargs):
        inplace = kwargs["inplace"] if "inplace" in kwargs.keys() else args[-1]
        if not inplace:
            if "df" in kwargs.keys():
                df = kwargs["df"]
                df_copy = df.copy()
                kwargs["df"] = df_copy
            else:
                # Convert
                df = args[0]
                df_copy = df.copy()
                kwargs["inplace"] = inplace
                kwargs["df"] = df_copy
                args = ()
        func(*args, **kwargs)
        if not inplace:
            return kwargs["df"] if "df" in kwargs.keys() else args[0]

    return inner


@inplace
def normalizeColumnsName(df: pd.DataFrame, inplace: bool):
    columns = df.columns
    normalized_columns = (normalizeColumn(col) for col in columns)
    df.columns = normalized_columns


def normalizeColumn(column: str) -> str:
    lowered_column = column.lower()
    normalized_column = lowered_column.replace(" ", "_")
    return normalized_column


@inplace
def selectColumns(df: pd.DataFrame, columns: typing.List[str], inplace: bool):
    df = df[df.columns.intersection(columns)]


@inplace
def replaceEmptyCellWithAboveCellForEachRow(
    df: pd.DataFrame, column: str, inplace: bool
) -> pd.DataFrame:
    above_value = df.at[0, column]
    for i in df.index[1:]:
        value = df.at[i, column]
        if pd.isnull(value):
            df.at[i, column] = above_value
        else:
            above_value = value


@inplace
def removeLinesWithEmptyColumn(df, column: str, inplace: bool):
    for i in range(len(df)):
        value = df.loc[i, column]
        if pd.isnull(value):
            df.drop(i, inplace=inplace)


@inplace
def applyStrTo(df, column: str, inplace: bool):
    df[column] = df[column].apply(str)


@inplace
def normalizeValuesOfColumns(df, column: str, inplace: bool):
    cleaners = [
        unidecode.unidecode,
        lambda text: text.lower(),
        lambda text: text.replace("'", "_"),
    ]
    for cleaner in cleaners:
        df[column] = df[column].apply(lambda x: cleaner(x) if not pd.isna(x) else x)


@inplace
def removeColumnsNotIn(
    df: pd.DataFrame, expected_columns: typing.List[str], inplace: bool
):
    for column in df.columns:
        normalized_column = normalizeColumn(column)
        if normalized_column not in expected_columns:
            df.pop(column)


@inplace
def removeColumnsNotInExpectedExcelColumns(df: pd.DataFrame, inplace: bool):
    return removeColumnsNotIn(df, EXCEL_COLUMNS, inplace)
