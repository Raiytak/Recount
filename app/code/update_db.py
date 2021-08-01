def updatingByRemovingAllExistingRowsOfTable(wrapperTable):
    def updateDecorator(func):
        def inner(*args, **kwargs):
            username = args[0]
            print(
                f"*-*-* Remove rows of '{wrapperTable.table}' for user '{username}' *-*-*"
            )
            with wrapperTable:
                wrapperTable.dumpTableForUser(username)
            return func(*args, **kwargs)

        return inner

    return updateDecorator


from accessors.access_config import AccessConfig

myAccessConfig = AccessConfig()
db_config = myAccessConfig.getDatabaseConfig()


from wrapper_excel.convert_excel_to_df import ExcelToDataframe
from wrapper_excel.cleaner_dataframe import CleanerDataframe
from wrapper_excel.fill_blanks import IntelligentFill, UpdateConversionJson
from wrapper_excel.check_conformity import ReviewerDataframe
from wrapper_excel.main_cleaner import MainCleanerExcel


myExcelToDataframe = ExcelToDataframe()
myCleanerDataframe = CleanerDataframe()
myIntelligentFill = IntelligentFill()
myReviewerDataframe = ReviewerDataframe()
mainCleaner = MainCleanerExcel(
    myExcelToDataframe, myCleanerDataframe, myIntelligentFill, myReviewerDataframe
)

myUpdateConversionJson = UpdateConversionJson()


from wrapper_sql.wrapper_sql import WrapperOfTable
from wrapper_sql.dataframe_to_request_sql import DataframeToSql
from wrapper_sql.response_to_dataframe import ResponseSqlToDataframe, ResponseSqlToList
from wrapper_sql.table_to_other_table import (
    RawToRepayement,
    RawToTrip,
    RawToClean,
    TripToClean,
)
from wrapper_sql.repay_repayments import RepayPepayements

convertDfToReq = DataframeToSql()
convertRespToDf = ResponseSqlToDataframe()
convertRespToList = ResponseSqlToList()

rawTable = WrapperOfTable("raw_expenses", db_config)
tripTable = WrapperOfTable("trip_expenses", db_config)
repayTable = WrapperOfTable("reimbursement", db_config)
cleanTable = WrapperOfTable("clean_expenses", db_config)

rawToRepayement = RawToRepayement(rawTable, repayTable)
rawToTrip = RawToTrip(rawTable, tripTable)
rawToClean = RawToClean(rawTable, cleanTable)
tripToClean = TripToClean(tripTable, cleanTable)

repayRep = RepayPepayements(rawTable, repayTable)


@updatingByRemovingAllExistingRowsOfTable(rawTable)
def updateRawTable(username):
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


@updatingByRemovingAllExistingRowsOfTable(repayTable)
def updateRepayementsTable(username):
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
    with rawTable:
        rawTable.deleteListRowsId(list_resp)


# TODO using username
def repayRepayements(username):
    print("--- Repay 'reimbursement' in 'raw_expenses' ---")
    with repayRep:
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
        dataframe_cleaned = repayRep.addDfRawAndDfRepayement(
            dataframe_raw, dataframe_rep
        )

        equivalent_columns = convertRespToDf.getEquivalentColumns(rawTable)
        requests_cleaned_rows = convertDfToReq.translateDataframeToRequestSql(
            dataframe_cleaned, equivalent_columns
        )
        repayRep.insertCleanedRowsReqs(requests_cleaned_rows)


@updatingByRemovingAllExistingRowsOfTable(tripTable)
def updateTripsTable(username):
    print("--- Update 'trip_expenses' ---")
    response = rawToTrip.selectTripRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToTrip.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(
        dataframe, equivalent_columns
    )
    rawToTrip.dumpTripTableForUser(username)
    rawToTrip.insertAllReqsInTrip(list_requests)


# TODO using username
def deleteTripsFromRaw(username):
    print("--- Delete 'trip_expenses' in 'raw_expenses' ---")
    response = rawToTrip.selectTripIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    with rawTable:
        rawTable.deleteListRowsId(list_resp)


@updatingByRemovingAllExistingRowsOfTable(cleanTable)
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
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print("--- User : '" + username + "' ---")
    updateRawTable(username)

    updateRepayementsTable(username)
    deleteRepayementsFromRaw(username)
    repayRepayements(username)

    updateTripsTable(username)
    deleteTripsFromRaw(username)

    updateCleanTable(username)
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
