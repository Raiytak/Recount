# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
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

# convertDfToReq = DataframeToSql()
# convertRespToDf = ResponseSqlToDataframe()
# convertRespToList = ResponseSqlToList()

# tripTable = WrapperOfTable("trip_expenses", db_config)
# repayTable = WrapperOfTable("reimbursement", db_config)
# cleanTable = WrapperOfTable("clean_expenses", db_config)


class UpdatePipeline:
    def __init__(self, username: str, db_config=None):
        self.username = username
        if db_config is None:
            db_config = access.AccessConfig.databaseConfig
        self.raw_table = com.UserSqlTable(username, "raw_expenses", db_config)
        # self.raw_table = com.UserSqlTable("raw_expenses", db_config)
        # self.raw_table = com.UserSqlTable("raw_expenses", db_config)
        # self.raw_table = com.UserSqlTable("raw_expenses", db_config)
        self.excel_to_dataframe = convert.ExcelToDataframe(username=username)
        self.intelligent_fill = cleaner.IntelligentFill(username=username)

    def getDataframeFromExcel(self):
        return self.excel_to_dataframe.getDataframe()

    def getEquivalentColumns(self):
        return self.excel_to_dataframe.getEquivalentColumns()

    def process(self):
        dataframe = self.getDataframeFromExcel()
        equivalent_columns = self.getEquivalentColumns()
        self.cleanDataframe(dataframe)
        self.updateRawTable(dataframe, equivalent_columns)

    def cleanDataframe(self, dataframe):
        cleaner.addDateEverywhere(dataframe)
        cleaner.convertDateToStr(dataframe)

        cleaner.removeLinesWithoutExpense(dataframe)

        cleaner.summarizeExpenses(dataframe)
        cleaner.convertExpensesToStr(dataframe)

        cleaner.normalizeDescription(dataframe)
        cleaner.splitAndCleanCategory(dataframe)
        cleaner.splitAndCleanDescription(dataframe)

        self.intelligent_fill.fillBlanks(dataframe)

        cleaner.removeUselessColumns(dataframe)
        cleaner.removeAllApostrophes(dataframe)

        cleaner.convertStrNanToNan(dataframe)

    def updateRawTable(self, dataframe, equivalent_columns):
        """Update table by removing all user entries"""
        logs.formatAndDisplay(f"@{self.username}: Update '{self.raw_table.table_name}'")
        self.dumpUserOfTable(self.raw_table)
        list_requests = convert.DataframeToSql.translateIntoInsertRequests(
            dataframe, equivalent_columns, self.raw_table.table_name
        )
        # TODO: Adapt to table columns (delete raw ?)
        self.raw_table.insertAllReqs(list_requests)

    def dumpUserOfTable(self, wrapperTable: com.UserSqlTable):
        logs.formatAndDisplay(
            f"@{self.username}: Remove rows of '{wrapperTable.table_name}'"
        )
        wrapperTable.dumpTable()


# def updateExcel(username):
#     """Copy the imported excel (if exists then remove it),
#     create a new excel that is used for cleaning the data that will then be uploaded on MySQL."""
#     logs.formatAndDisplay(f"{username}: Update excel files")
#     mainCleaner = MainCleanerExcel(username)
#     try:
#         mainCleaner.updateExcel()
#     except Exception as exp:
#         logs.formatAndDisplay(f"The excel files created errors: {exp}")
#         return False
#     return True


# @dumpUserOfTable(repayTable)
# def updateRepayementsTable(username):
#     logs.formatAndDisplay(f"{username}: Update 'reimbursement' Table")
#     rawToRepayement = RawToRepayement(raw_table, repayTable, username)
#     response = rawToRepayement.selectRepayementRows()
#     dataframe = convertRespToDf.translateResponseSqlToDataframe(response, raw_table)
#     equivalent_columns = rawToRepayement.getEquivalentColumns()
#     list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
#         dataframe, equivalent_columns
#     )
#     repayTable.insertAllReqs(list_requests)


# # TODO verify use username
# def deleteRepayementsFromRaw(username):
#     logs.formatAndDisplay(f"{username}: Delete 'reimbursement' in 'raw_expenses'")
#     rawToRepayement = RawToRepayement(raw_table, repayTable, username)
#     response = rawToRepayement.selectRepayementIds()
#     list_resp = convertRespToList.translateResponseSqlToList(response)
#     with raw_table:
#         raw_table.deleteListRowsId(list_resp)


# # TODO verify use username
# def repayRepayements(username):
#     logs.formatAndDisplay(f"{username}: Repay 'reimbursement' in 'raw_expenses'")
#     repayRep = RepayPepayements(raw_table, repayTable, username)
#     with repayRep:
#         response_rep = repayRep.selectRepayementRows()
#         dataframe_rep = convertRespToDf.translateResponseSqlToDataframe(
#             response_rep, repayTable
#         )

#         list_ids_pay_orig = repayRep.convertDataframeToListIdsPayOrig(dataframe_rep)
#         response_raw = repayRep.selectRowsOfRawWithId(list_ids_pay_orig)
#         repayRep.deleteRowsOfRawIds(list_ids_pay_orig)

#         dataframe_raw = convertRespToDf.translateResponseSqlToDataframe(
#             response_raw, raw_table
#         )
#         dataframe_cleaned = repayRep.addDfRawAndDfRepayement(
#             dataframe_raw, dataframe_rep
#         )

#         equivalent_columns = convertRespToDf.getEquivalentColumns(raw_table)
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
#     rawToTrip = RawToTrip(raw_table, tripTable, username)
#     response = rawToTrip.selectTripRows()
#     dataframe = convertRespToDf.translateResponseSqlToDataframe(response, raw_table)
#     equivalent_columns = rawToTrip.getEquivalentColumns()
#     list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
#         dataframe, equivalent_columns
#     )
#     rawToTrip.insertAllReqsInTrip(list_requests)


# def deleteTripsFromRaw(username):
#     logs.formatAndDisplay(f"{username}: Delete 'trip_expenses' in 'raw_expenses'")
#     rawToTrip = RawToTrip(raw_table, tripTable, username)
#     response = rawToTrip.selectTripIds()
#     list_resp = convertRespToList.translateResponseSqlToList(response)
#     with raw_table:
#         raw_table.deleteListRowsId(list_resp)


# @dumpUserOfTable(cleanTable)
# def updateCleanTable(username):
#     logs.formatAndDisplay(f"{username}: Update 'clean_expenses'")
#     rawToClean = RawToClean(raw_table, cleanTable, username)
#     response = rawToClean.selectAllRemainingRowsInRaw()
#     dataframe = convertRespToDf.translateResponseSqlToDataframe(response, raw_table)
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
#     raw_table.dumpTableForUser(username)
#     repayTable.dumpTableForUser(username)
#     tripTable.dumpTableForUser(username)
#     cleanTable.dumpTableForUser(username)


# def removeAllExcelsForUser(username):
#     myAccessUserFiles = access.AccessUserFiles(username)
#     myAccessUserFiles.removeExcelsOfUser()


# def removeAllExcelsExceptRawForUser(username):
#     myAccessUserFiles = access.AccessUserFiles(username)
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
