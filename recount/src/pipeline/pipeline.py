# -*- coding: utf-8 -*-
# TODO: update description
""" 
                    ====     DESCRIPTION    ====
TODO: redo comments
Contains the logic used to update the excels and the SQL data.

On the excel part:
    -raw_excel:      excel that contains the data given by the user
    -imported_excel: data uploaded by the user, copied then removed
    -clean_excel:    excel used for the converion to MySQL, then removed

On the MySQL part:
    -raw_expenses:      data imported from clean_excel
    -reimbursement:     table containing the rows used for reimbursement
    -trip_expenses:     table containing the rows of the different trips
    -clean_expenses:    data cleaned, used to create graphs
"""

import logs
import com
import access

import pipeline.convert as convert
import pipeline.cleaner as cleaner
import pipeline.check as check


# TODO: test
class UpdatePipeline:
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
        self.df_to_sql = convert.DataframeToSql(self.equivalent_columns)
        self.intelligent_fill = cleaner.IntelligentFill(
            self.user_files.intelligent_fill
        )
        self.cleaner_dataframe = cleaner.CleanerDataframe(self.equivalent_columns)

    def getDataframeFromExcel(self):
        return self.user_files.dataframe()

    def process(self):
        dataframe = self.getDataframeFromExcel()
        self.cleanDataframe(dataframe)
        self.updateRawTable(dataframe)

    def cleanDataframe(self, dataframe):
        self.cleaner_dataframe.addDateEverywhere(dataframe)
        self.cleaner_dataframe.addCurrencyEverywhere(dataframe)

        self.cleaner_dataframe.removeLinesWithoutAmount(dataframe)

        # self.cleaner_dataframe.convertAmountWithCurrencyAndDateIntoEuro(dataframe)
        self.cleaner_dataframe.convertAmountToStr(dataframe)

        self.cleaner_dataframe.splitAndCleanDescription(dataframe)
        self.cleaner_dataframe.normalizeDescription(dataframe)
        self.cleaner_dataframe.normalizeCompany(dataframe)

        self.intelligent_fill.fillBlanks(dataframe)

        self.cleaner_dataframe.normalizeImportantColumns(dataframe)
        self.cleaner_dataframe.removeUselessColumns(dataframe)

        self.cleaner_dataframe.convertStrNanToNan(dataframe)

    def updateRawTable(self, dataframe):
        """Update table by removing all user entries"""
        logs.formatAndDisplay(
            f"@{self.username}: Update '{self.expense_table.table_name}'"
        )
        # self.dumpUserOfTable(self.expense_table)
        list_requests = self.df_to_sql.translateDataframeIntoInsertRequests(
            dataframe, self.expense_table
        )
        print(list_requests)
        # self.expense_table.insertAllReqs(list_requests)

    def dumpUserOfTable(self, wrapperTable: com.UserSqlTable):
        logs.formatAndDisplay(
            f"@{self.username}: Remove rows of '{wrapperTable.table_name}'"
        )
        wrapperTable.dumpTable()


# @dumpUserOfTable(repayTable)
# def updateRepayementsTable(username):
#     logs.formatAndDisplay(f"{username}: Update 'reimbursement' Table")
#     rawToRepayement = RawToRepayement(expense_table, repayTable, username)
#     response = rawToRepayement.selectRepayementRows()
#     dataframe = convertRespToDf.translateResponseSqlToDataframe(response, expense_table)
#     equivalent_columns = rawToRepayement.getEquivalentColumns()
#     list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
#         dataframe, equivalent_columns
#     )
#     repayTable.insertAllReqs(list_requests)


# # TODO verify use username
# def deleteRepayementsFromRaw(username):
#     logs.formatAndDisplay(f"{username}: Delete 'reimbursement' in 'raw_expenses'")
#     rawToRepayement = RawToRepayement(expense_table, repayTable, username)
#     response = rawToRepayement.selectRepayementIds()
#     list_resp = convertRespToList.translateResponseSqlToList(response)
#     with expense_table:
#         expense_table.deleteListRowsId(list_resp)


# # TODO verify use username
# def repayRepayements(username):
#     logs.formatAndDisplay(f"{username}: Repay 'reimbursement' in 'raw_expenses'")
#     repayRep = RepayPepayements(expense_table, repayTable, username)
#     with repayRep:
#         response_rep = repayRep.selectRepayementRows()
#         dataframe_rep = convertRespToDf.translateResponseSqlToDataframe(
#             response_rep, repayTable
#         )

#         list_ids_pay_orig = repayRep.convertDataframeToListIdsPayOrig(dataframe_rep)
#         response_raw = repayRep.selectRowsOfRawWithId(list_ids_pay_orig)
#         repayRep.deleteRowsOfRawIds(list_ids_pay_orig)

#         dataframe_raw = convertRespToDf.translateResponseSqlToDataframe(
#             response_raw, expense_table
#         )
#         dataframe_cleaned = repayRep.addDfRawAndDfRepayement(
#             dataframe_raw, dataframe_rep
#         )

#         equivalent_columns = convertRespToDf.getEquivalentColumns(expense_table)
#         requests_cleaned_rows = convertDfToReq.translateDataframeToInsertRequestSql(
#             dataframe_cleaned, equivalent_columns
#         )
#         # Updating by removing old values, TODO
#         list_ids_pay_reimb = repayRep.convertDataframeToListIdsPayOrig(dataframe_rep)
#         repayRep.deleteRowsOfRawIds(list_ids_pay_reimb)
#         repayRep.insertCleanedRowsReqs(requests_cleaned_rows)


# @dumpUserOfTable(tripTable)
# def updateTripsTable(username):
#     logs.formatAndDisplay(f"{username}: Update 'trip_expenses'")
#     rawToTrip = RawToTrip(expense_table, tripTable, username)
#     response = rawToTrip.selectTripRows()
#     dataframe = convertRespToDf.translateResponseSqlToDataframe(response, expense_table)
#     equivalent_columns = rawToTrip.getEquivalentColumns()
#     list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
#         dataframe, equivalent_columns
#     )
#     rawToTrip.insertAllReqsInTrip(list_requests)


# def deleteTripsFromRaw(username):
#     logs.formatAndDisplay(f"{username}: Delete 'trip_expenses' in 'raw_expenses'")
#     rawToTrip = RawToTrip(expense_table, tripTable, username)
#     response = rawToTrip.selectTripIds()
#     list_resp = convertRespToList.translateResponseSqlToList(response)
#     with expense_table:
#         expense_table.deleteListRowsId(list_resp)


# @dumpUserOfTable(cleanTable)
# def updateCleanTable(username):
#     logs.formatAndDisplay(f"{username}: Update 'clean_expenses'")
#     rawToClean = RawToClean(expense_table, cleanTable, username)
#     response = rawToClean.selectAllRemainingRowsInRaw()
#     dataframe = convertRespToDf.translateResponseSqlToDataframe(response, expense_table)
#     equivalent_columns = rawToClean.getEquivalentColumns()
#     list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
#         dataframe, equivalent_columns
#     )

#     logs.formatAndDisplay(f"{username}: Adding trip expenses")
#     tripToClean = TripToClean(tripTable, cleanTable, username)
#     response = tripToClean.selectAllRemainingRowsInTrip()
#     dataframe = convertRespToDf.translateResponseSqlToDataframe(response, tripTable)
#     equivalent_columns = tripToClean.getEquivalentColumns()
#     list_requests += convertDfToReq.translateDataframeToInsertRequestSql(
#         dataframe, equivalent_columns
#     )
#     cleanTable.insertAllReqs(list_requests)


# def updateSqlDb(username):
#     dataframe = getExcel()

#     updateExcel(username)

#     updateRawTable(username)

#     updateRepayementsTable(username)
#     deleteRepayementsFromRaw(username)
#     repayRepayements(username)

#     updateTripsTable(username)
#     deleteTripsFromRaw(username)

#     updateCleanTable(username)
#     logs.formatAndDisplay("")


# def removeAllDataForUser(username):
#     removeAllExcelsForUser(username)
#     removeAllSqlDataForUser(username)


# def removeAllSqlDataForUser(username):
#     expense_table.dumpTableForUser(username)
#     repayTable.dumpTableForUser(username)
#     tripTable.dumpTableForUser(username)
#     cleanTable.dumpTableForUser(username)


# def removeAllExcelsForUser(username):
#     myAccessUserFiles = access.UserFilesAccess(username)
#     myAccessUserFiles.removeExcelsOfUser()


# def removeAllExcelsExceptRawForUser(username):
#     myAccessUserFiles = access.UserFilesAccess(username)
#     myAccessUserFiles.removeExcelsExceptRawOfUser()


# def updateAll(username):
#     """Updates all the tables of the given user.
#     For now it removes ALL the older values."""
#     # TODO: improve remove ALL -> update values
#     # TODO: use cache
#     # TODO: use data encryption
#     logs.formatAndDisplay("")
#     sql_is_to_update = updateExcel(username)
#     if sql_is_to_update == True:
#         updateSqlDb(username)
