# def updatingByRemovingAllExistingRowsOfTable(wrapperTable):
#     def updateDecorator(func):
#         def inner(*args, **kwargs):
#             print("**kwargs")
#             print(kwargs)
#             wrapperTable.dumpTable()
#             return func(*args, **kwargs)
#         return inner
#     return updateDecorator

import re
import os


def get_code_path():
    path_file = os.path.abspath(__file__)
    path_app = re.sub("(app).*", "app", path_file)
    path_code = os.path.join(path_app, "code")
    return path_code


# To use if having trouble relying on sys.path automatic linking
os.environ["CODE_PATH"] = get_code_path()

from accessors.access_config import AccessConfig

myAccessConfig = AccessConfig()
config_json = myAccessConfig.getConfig()

from accessors.path_files import (
    ExcelPath,
    DescrToThemePath,
    CategoryAndThemeAuthorizedPath,
)

myExcelPath = ExcelPath()
myDescrToThemePath = DescrToThemePath()
myCatThemeAuthPath = CategoryAndThemeAuthorizedPath()

from accessors.access_files import AccessDescrToTheme, AccessCTAuthorized, AccessExcel

myAccessDescrToTheme = AccessDescrToTheme(myDescrToThemePath)
myAccessCTAuthorized = AccessCTAuthorized(myCatThemeAuthPath)
myAccessExcel = AccessExcel(myExcelPath)


import wrapper_excel.convert_excel_to_df as convert_excel_to_df
import wrapper_excel.main_cleaner as main_cleaner
import wrapper_excel.cleaner_dataframe as cleaner_dataframe
import wrapper_excel.fill_blanks as fill_blanks
import wrapper_excel.check_conformity as check_conformity


myExcelToDataframe = convert_excel_to_df.ExcelToDataframe(myAccessExcel)
myCleanerDataframe = cleaner_dataframe.CleanerDataframe()
myIntelligentFill = fill_blanks.IntelligentFill(myAccessDescrToTheme)
myReviewerDataframe = check_conformity.ReviewerDataframe(myAccessCTAuthorized)
mainCleaner = main_cleaner.MainCleanerExcel(
    myExcelToDataframe, myCleanerDataframe, myIntelligentFill, myReviewerDataframe
)

myUpdateConversionJson = fill_blanks.UpdateConversionJson(myAccessDescrToTheme)


import wrapper_sql.wrapper_sql as wrapper_sql
import wrapper_sql.dataframe_to_request_sql as dataframe_to_request_sql
import wrapper_sql.response_to_dataframe as response_to_dataframe
import wrapper_sql.table_to_other_table as table_to_other_table
import wrapper_sql.repay_repayments as repay_repayments

convertDfToReq = dataframe_to_request_sql.DataframeToSql()
convertRespToDf = response_to_dataframe.ResponseSqlToDataframe()
convertRespToList = response_to_dataframe.ResponseSqlToList()

rawTable = wrapper_sql.WrapperOfTable("raw_expenses", config_json)
tripTable = wrapper_sql.WrapperOfTable("trip_expenses", config_json)
repayTable = wrapper_sql.WrapperOfTable("reimbursement", config_json)
cleanTable = wrapper_sql.WrapperOfTable("clean_expenses", config_json)

rawToRepayement = table_to_other_table.RawToRepayement(rawTable, repayTable)
rawToTrip = table_to_other_table.RawToTrip(rawTable, tripTable)
rawToClean = table_to_other_table.RawToClean(rawTable, cleanTable)
tripToClean = table_to_other_table.TripToClean(tripTable, cleanTable)

repayRep = repay_repayments.RepayPepayements(rawTable, repayTable)


# @updatingByRemovingAllExistingRowsOfTable(rawTable)
def updateRawTable(username):
    print("--- User : '" + username + "' ---")
    print("--- Update 'raw_expenses' Table ---")
    mainCleaner.updateExcel()
    dataframe, equivalent_columns = mainCleaner.getDataframeAndEqCol()
    dataframe["username"] = username
    myUpdateConversionJson.updateConversionJsonUsingDataframe(dataframe)
    list_requests = convertDfToReq.translateDataframeToRequestSql(
        dataframe, equivalent_columns
    )

    rawTable.dumpTableForUser(username)
    rawTable.insertAllReqs(list_requests)


# @updatingByRemovingAllExistingRowsOfTable(repayTable)
def updateRepayementsTable(username):
    print("--- User : '" + username + "' ---")
    print("--- Update 'reimbursement' Table ---")
    response = rawToRepayement.selectRepayementRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToRepayement.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(
        dataframe, equivalent_columns
    )

    repayTable.dumpTableForUser(username)
    repayTable.insertAllReqs(list_requests)


# TODO using username
def deleteRepayementsFromRaw(username):
    print("--- Delete 'reimbursement' in 'raw_expenses' ---")
    response = rawToRepayement.selectRepayementIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    rawTable.deleteListRowsId(list_resp)


# TODO using username
def repayRepayements(username):
    print("--- Repay 'reimbursement' in 'raw_expenses' ---")
    response_rep = repayRep.selectRepayementRows()
    dataframe_rep = convertRespToDf.translateResponseSqlToDataframe(
        response_rep, repayTable
    )

    list_ids_pay_orig = repayRep.convertDataframeToListIdsPayOrig(dataframe_rep)
    response_raw = repayRep.selectRowsOfRawWhereIds(list_ids_pay_orig)
    repayRep.deleteRowsOfRawWhereIds(list_ids_pay_orig)

    dataframe_raw = convertRespToDf.translateResponseSqlToDataframe(
        response_raw, rawTable
    )
    dataframe_cleaned = repayRep.addDfRawAndDfRepayement(dataframe_raw, dataframe_rep)

    equivalent_columns = convertRespToDf.getEquivalentColumns(rawTable)
    requests_cleaned_rows = convertDfToReq.translateDataframeToRequestSql(
        dataframe_cleaned, equivalent_columns
    )
    repayRep.insertCleanedRowsReqs(requests_cleaned_rows)


# @updatingByRemovingAllExistingRowsOfTable(tripTable)
def updateTripsTable(username):
    print("--- Update 'trip_expenses' ---")
    response = rawToTrip.selectTripRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToTrip.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(
        dataframe, equivalent_columns
    )

    tripTable.dumpTableForUser(username)
    tripTable.insertAllReqs(list_requests)


# TODO using username
def deleteTripsFromRaw(username):
    print("--- Delete 'trip_expenses' in 'raw_expenses' ---")
    response = rawToTrip.selectTripIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    rawTable.deleteListRowsId(list_resp)


# @updatingByRemovingAllExistingRowsOfTable(cleanTable)
def updateCleanTable(username):
    print("--- Update 'clean_expenses' ---")
    response = rawToClean.selectAllRemainingRowsInRaw()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToClean.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(
        dataframe, equivalent_columns
    )

    print("--- Adding trip expenses ---")
    response = tripToClean.selectAllRemainingRowsInTrip()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, tripTable)
    equivalent_columns = tripToClean.getEquivalentColumns()
    list_requests += convertDfToReq.translateDataframeToRequestSql(
        dataframe, equivalent_columns
    )

    cleanTable.dumpTableForUser(username)
    cleanTable.insertAllReqs(list_requests)


# == MAIN == FUNCTION : updates all the tables by removing ALL the older values
def updateAll(username):
    updateRawTable(username)

    updateRepayementsTable(username)
    deleteRepayementsFromRaw(username)
    repayRepayements(username)

    updateTripsTable(username)
    deleteTripsFromRaw(username)

    updateCleanTable(username)
