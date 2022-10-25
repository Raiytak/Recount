import typing
import pandas as pd
import unidecode


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
    lowered_columns = (col.lower() for col in columns)
    normalized_columns = (col.replace(" ", "_") for col in lowered_columns)
    df.columns = normalized_columns


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
def normalizeColumn(df, column: str, inplace: bool):
    cleaners = [
        unidecode.unidecode,
        lambda text: text.lower(),
        lambda text: text.replace("'", "_"),
    ]
    for cleaner in cleaners:
        df[column] = df[column].apply(lambda x: cleaner(x) if not pd.isna(x) else x)

