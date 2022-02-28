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

import logs
import com
import access

import pipeline.convert as convert
import pipeline.cleaner as cleaner
import pipeline.check as check
from src.pipeline.cleaner.intelligent_fill import updateUserIntelligentFill


class UpdateDatabase:
    def __init__(self, username: str, db_config=None):
        self.username = username
        if db_config is None:
            db_config = access.ConfigAccess.database_config

        self.expense_table = com.UserSqlTable(username, com.Table.EXPENSE, db_config)
        self.reimbursement_table = com.UserSqlTable(
            username, com.Table.REIMBURSEMENT, db_config
        )

        self.user_files = access.UserFilesAccess(username=username)
        self.equivalent_columns = self.user_files.equivalent_columns
        self.cleaner_dataframe = cleaner.CleanerDataframe(self.equivalent_columns)

    def getDataframeFromExcel(self):
        dataframe = self.user_files.dataframe()
        dataframe["username"] = self.username
        return dataframe

    def updateData(self):
        dataframe = self.getDataframeFromExcel()
        self.cleanDataframe(dataframe)
        self.updateIntelligentFill(dataframe)
        self.updateExpenseTable(dataframe)
        self.updateReimbursementTable(dataframe)

    def cleanDataframe(self, dataframe):
        self.cleaner_dataframe.addDateEverywhere(dataframe)
        self.cleaner_dataframe.addCurrencyEverywhere(dataframe)

        self.cleaner_dataframe.removeLinesWithoutAmount(dataframe)

        # self.cleaner_dataframe.convertAmountWithCurrencyAndDateIntoEuro(dataframe)
        self.cleaner_dataframe.convertAmountToStr(dataframe)

        self.cleaner_dataframe.splitAndCleanDescription(dataframe)
        self.cleaner_dataframe.normalizeDescription(dataframe)
        self.cleaner_dataframe.normalizeCompany(dataframe)

        self.cleaner_dataframe.normalizeColumnsName(dataframe)
        self.cleaner_dataframe.removeUselessColumns(dataframe)

        cleaner.fillBlanks(dataframe, self.user_files)

    def updateIntelligentFill(self, dataframe):
        logs.formatAndDisplay(f"@{self.username}: Update 'intelligent fill'")
        updateUserIntelligentFill(dataframe, self.user_files)

    def updateExpenseTable(self, dataframe):
        logs.formatAndDisplay(
            f"@{self.username}: Update '{self.expense_table.table_name}'"
        )
        self.dumpUserOfTable(self.expense_table)

        is_expense = dataframe["reimbursement"].isna()
        df = dataframe[self.expense_table.columns_name]
        expense_df = df[is_expense]
        list_requests = convert.translateDataframeIntoInsertRequests(
            expense_df, self.expense_table
        )
        self.expense_table.insertAllReqs(list_requests)

    def updateReimbursementTable(self, dataframe):
        logs.formatAndDisplay(
            f"@{self.username}: Update '{self.reimbursement_table.table_name}'"
        )
        self.dumpUserOfTable(self.reimbursement_table)

        is_expense = dataframe["reimbursement"].notna()
        dataframe.rename(columns={"reimbursement": "ID_origin"}, inplace=True)
        df = dataframe[self.reimbursement_table.columns_name]
        expense_df = df[is_expense]
        list_requests = convert.translateDataframeIntoInsertRequests(
            expense_df, self.reimbursement_table
        )
        self.reimbursement_table.insertAllReqs(list_requests)

    def dumpUserOfTable(self, wrapperTable: com.UserSqlTable):
        logs.formatAndDisplay(
            f"@{self.username}: Truncate table '{wrapperTable.table_name}' for user '{self.username}'"
        )
        wrapperTable.dumpTable()
