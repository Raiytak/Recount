import pandas as pd

from accessors import UserManager
from interface.dash_interface import *


class DashManager:
    MAIN_CATEGORY = "main_category"
    ALIMENTARY_CATEGORY = "alimentary_category"

    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    @staticmethod
    def cleanDf(df: pd.DataFrame) -> None:
        removeEmptyCategories(df)
        DashManager.insertMainCategoryInDf(df)
        DashManager.insertAlimentaryCategoryInDf(df)

    @staticmethod
    def insertMainCategoryInDf(df: pd.DataFrame) -> None:
        main_categories = getMainCategoriesOfDf(df)
        df.insert(0, DashManager.MAIN_CATEGORY, main_categories)

    @staticmethod
    def insertAlimentaryCategoryInDf(df: pd.DataFrame) -> None:
        main_categories = getAlimentaryCategoriesOfDf(df)
        df.insert(0, DashManager.ALIMENTARY_CATEGORY, main_categories)

    @staticmethod
    def expensesByCategory(df: pd.DataFrame) -> list:
        return dataframeToExpensesByColumn(df, DashManager.MAIN_CATEGORY)

    @staticmethod
    def expensesByCategory(df: pd.DataFrame) -> list:
        return dataframeToExpensesByColumn(df, DashManager.MAIN_CATEGORY)

    @staticmethod
    def sumExpensesByCategory(df: pd.DataFrame) -> dict:
        return dataframeToSumExpensesByColumn(df, DashManager.MAIN_CATEGORY)

    @staticmethod
    def sumExpensesByCategoryByPeriod(df: pd.DataFrame, selected_period: str) -> list:
        return dataframeToSumExpensesByPeriodAndColumn(
            df, DashManager.MAIN_CATEGORY, selected_period
        )

    @staticmethod
    def sumExpensesAlimentaryByPeriod(df: pd.DataFrame, selected_period: str) -> list:
        return dataframeToSumExpensesByPeriodAndColumn(
            df, DashManager.ALIMENTARY_CATEGORY, selected_period
        )
