import pandas as pd

from accessors import UserManager
from interface.dash_interface import *


class DashManager:
    MAIN_CATEGORY = "main_category"

    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    @staticmethod
    def cleanDf(df: pd.DataFrame) -> None:
        removeEmptyCategories(df)
        DashManager.insertMainCategoryInDf(df)

    @staticmethod
    def insertMainCategoryInDf(df: pd.DataFrame) -> None:
        main_categories = getMainCategoriesOfDf(df)
        df.insert(0, DashManager.MAIN_CATEGORY, main_categories)

    @staticmethod
    def expensesByCategory(df: pd.DataFrame) -> list:
        return dataframeToExpensesByColumn(df, DashManager.MAIN_CATEGORY)

    @staticmethod
    def sumExpensesByCategory(df: pd.DataFrame) -> dict:
        return dataframeToSumExpensesByColumn(df, DashManager.MAIN_CATEGORY)
