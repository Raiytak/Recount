import pandas as pd
import unidecode


def replaceEmptyCellWithAboveCellForEachRow(
    df: pd.DataFrame, column: str, inplace: bool = False
) -> pd.DataFrame:
    if not inplace:
        df = df.copy()
    above_value = df.loc[0, column]
    for i in range(1, len(df)):
        value = df.loc[i, column]
        if pd.isnull(value):
            df.at[i, column] = above_value
        else:
            above_value = value

    if not inplace:
        return df


def removeLinesWithEmptyColumn(df, column: str, inplace: bool = False):
    for i in range(len(df)):
        value = df.loc[i, column]
        if pd.isnull(value):
            df.drop(i, inplace=inplace)
    if not inplace:
        return df


def applyStrTo(df, column: str, inplace: bool = False):
    if not inplace:
        df = df.copy()
    df[column] = df[column].apply(str)
    if not inplace:
        return df


def normalizeColumn(df, column: str, inplace: bool = False):
    cleaners = [
        unidecode.unidecode,
        lambda text: text.lower(),
        lambda text: text.replace("'", "_"),
    ]
    for cleaner in cleaners:
        df[column] = df[column].apply(cleaner)

