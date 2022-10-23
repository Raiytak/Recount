# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Contains the logic used to update the database and to convert SQL requests into 

On the excel part:
    -expenses:      excel that contains the data given by the user

On the MySQL part:
    -expense:           data imported and cleaned from the user's excel
    -reimbursement:     table containing the reimbursement rows
"""

# from typing import List

# import logging
# import database
# import accessors

from src.interfaces.excel_interface import ExcelColumns
from cleaner import *


# import pipeline.convert as convert
# import pipeline.old_cleaner as old_cleaner
# import pipeline.check as check
# from pipeline.old_cleaner.intelligent_fill import updateUserIntelligentFill


class Pipeline:
    @staticmethod
    def cleanDf(df, inplace: bool = False):
        removeLinesWithEmptyColumn(df, ExcelColumns.CURRENCY, inplace)

        replaceEmptyCellWithAboveCellForEachRow(df, ExcelColumns.AMOUNT, inplace)
        replaceEmptyCellWithAboveCellForEachRow(df, ExcelColumns.CURRENCY, inplace)

        applyStrTo(df, ExcelColumns.AMOUNT, inplace)

        normalizeColumn(df, ExcelColumns.CATEGORY, inplace)
        normalizeColumn(df, ExcelColumns.DESCRITPION, inplace)
        normalizeColumn(df, ExcelColumns.PLACE, inplace)
        normalizeColumn(df, ExcelColumns.PAYEMENT_METHOD, inplace)
        normalizeColumn(df, ExcelColumns.RECEIVER, inplace)


# \\\\\\\\\\\\\\\\\\\\\


# class OldPipeline:
#     def __init__(self, username: str, db_config=None, *args, **kwargs):
#         self.username = username
#         if db_config is None:
#             db_config = accessors.ConfigManager.database_config_sql

#         self.expense_table = database.UserSqlTable(
#             username, database.Table.EXPENSE, db_config
#         )
#         self.reimbursement_table = database.UserSqlTable(
#             username, database.Table.REIMBURSEMENT, db_config
#         )

#         self.user_files = accessors.UserFolder(username=username)
#         self.equivalent_columns = self.user_files.equivalent_columns


# class UserDataPipeline(Pipeline):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.cleaner_dataframe = old_cleaner.CleanerDataframe(self.equivalent_columns)

#     def getDataframeFromExcel(self):
#         dataframe = self.user_files.dataframe()
#         dataframe["username"] = self.username
#         return dataframe

#     def updateData(self):
#         dataframe = self.getDataframeFromExcel()
#         self.cleanDataframe(dataframe)
#         self.updateExpenseTable(dataframe)
#         self.updateReimbursementTable(dataframe)

#     def cleanDataframe(self, dataframe):
#         self.cleaner_dataframe.addDateEverywhere(dataframe)
#         self.cleaner_dataframe.addCurrencyEverywhere(dataframe)

#         self.cleaner_dataframe.removeLinesWithoutAmount(dataframe)

#         # self.cleaner_dataframe.convertAmountWithCurrencyAndDateIntoEuro(dataframe)
#         self.cleaner_dataframe.convertAmountToStr(dataframe)

#         self.cleaner_dataframe.splitAndCleanDescription(dataframe)
#         self.cleaner_dataframe.normalizeDescription(dataframe)
#         self.cleaner_dataframe.normalizeCompany(dataframe)

#         self.cleaner_dataframe.normalizeColumnsName(dataframe)
#         self.cleaner_dataframe.removeUselessColumns(dataframe)

#         # cleaner.fillBlanks(dataframe, self.user_files)

#     def updateIntelligentFill(self, dataframe):
#         logging.info("@{}: Update 'intelligent fill'".format(self.username))
#         updateUserIntelligentFill(dataframe, self.user_files)

#     def updateExpenseTable(self, dataframe):
#         logging.info(
#             "@{}: Update '{}'".format(self.username, self.expense_table.table_name)
#         )
#         self.dumpUserOfTable(self.expense_table)

#         is_expense = dataframe["reimbursement"].isna()
#         df = dataframe[self.expense_table.columns_name]
#         expense_df = df[is_expense]
#         list_requests = convert.translateDataframeIntoInsertRequests(
#             expense_df, self.expense_table
#         )
#         self.expense_table.insertAllReqs(list_requests)
#         logging.info(
#             "@{}: Update '{}' done!".format(
#                 self.username, self.expense_table.table_name
#             )
#         )

#     def updateReimbursementTable(self, dataframe):
#         logging.info(
#             "@{}: Update '{}'".format(
#                 self.username, self.reimbursement_table.table_name
#             )
#         )
#         self.dumpUserOfTable(self.reimbursement_table)

#         is_expense = dataframe["reimbursement"].notna()
#         dataframe.rename(columns={"reimbursement": "ID_origin"}, inplace)
#         df = dataframe[self.reimbursement_table.columns_name]
#         expense_df = df[is_expense]
#         # TODO: set abs
#         # float_amounts = expense_df["amount"].astype(float).copy()
#         # expense_df.update(float_amounts.abs().copy())
#         list_requests = convert.translateDataframeIntoInsertRequests(
#             expense_df, self.reimbursement_table
#         )
#         self.reimbursement_table.insertAllReqs(list_requests)
#         logging.info(
#             "@{}: Update '{}' done!".format(
#                 self.username, self.reimbursement_table.table_name
#             )
#         )

#     def dumpUserOfTable(self, wrapperTable: database.UserSqlTable):
#         logging.info(
#             "@{}: Truncate table '{}'".format(self.username, wrapperTable.table_name)
#         )
#         wrapperTable.truncateTableOfUser()

#     def dumpUserOfAllTables(self):
#         logging.info("@{}: Truncate ALL tables".format(self.username))
#         self.dumpUserOfTable(self.expense_table)
#         self.dumpUserOfTable(self.reimbursement_table)


# class UserGraphPipeline(Pipeline):
#     def getExpenseRepaidForPeriod(self, start_date: str, end_date: str):
#         expense_df = self.getExpenseDataframeForPeriod(start_date, end_date)
#         reimbursement_df = self.getReimbursementDataframe()
#         return self.mergeExpenseAndReimbursement(expense_df, reimbursement_df)

#     def getExpenseDataframeForPeriod(self, start_date: str, end_date: str):
#         """The dates should be in format '%Y-%m-%d'"""
#         dataframe = convert.convertDateToDataframe(
#             start_date, end_date, self.expense_table
#         )
#         return dataframe

#     def getReimbursementDataframe(self):
#         dataframe = convert.translateSelectResponseToDataframe(
#             self.reimbursement_table.selectAll(), self.reimbursement_table
#         )
#         return dataframe

#     def mergeExpenseAndReimbursement(self, expense_df, reimbursement_df):
#         for idx, row in reimbursement_df.iterrows():
#             id = row["ID_origin"]
#             reimbursement = row["amount"]
#             if id in expense_df.index:
#                 expense_df.loc[id, "amount"] -= reimbursement
#         merged_df = expense_df[expense_df["amount"] > 0.1]
#         return merged_df

#     def getDataByColumn(self, dataframe, column="category") -> List[dict]:
#         data = convert.convertDataframeToGraphDataForEachUniqValueInColumn(
#             dataframe, column
#         )
#         return data

#     @staticmethod
#     def getDataByDateDeltaAndColumn(dataframe, column="category") -> List[dict]:
#         data = convert.converDataframeToDataGroupedByDateDeltaAndColumn(
#             dataframe, column
#         )
#         return data

#     @staticmethod
#     def getSumDataByColumn(dataframe, column="category") -> List[dict]:
#         data = convert.convertDataframeToSumDataForEachUniqValueInColumn(
#             dataframe, column
#         )
#         return data

#     @staticmethod
#     def selectMainCategory(category):
#         if type(category) != str:
#             return category
#         splitted_categories = category.split(":")
#         main_cat = splitted_categories[0]
#         return main_cat

#     @staticmethod
#     def selectSecondCategory(category):
#         splitted_categories = category.split(":")
#         if len(splitted_categories) > 1:
#             return splitted_categories[1]
#         return category

