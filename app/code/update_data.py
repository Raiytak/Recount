from genericpath import exists
import logging
from logs.logs import paddedLogMessage
from accessors.access_config import AccessConfig


def updatingByRemovingAllExistingRowsOfTable(wrapperTable):
    def updateDecorator(func):
        def inner(*args, **kwargs):
            username = args[0]
            logging.info(
                paddedLogMessage(f"@{username}: Remove rows of '{wrapperTable.table}'")
            )
            with wrapperTable:
                wrapperTable.dumpTableForUser(username)
                func(*args, **kwargs)

        return inner

    return updateDecorator


myAccessConfig = AccessConfig()
db_config = myAccessConfig.getDatabaseConfig()


from wrapper_excel.main_cleaner import MainCleanerExcel

from wrapper_excel.fill_blanks import UpdateConversionJson

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


def updateExcel(username):
    logging.info(paddedLogMessage(f"{username}: Update excel files"))
    mainCleaner = MainCleanerExcel(username)
    mainCleaner.updateExcel()


@updatingByRemovingAllExistingRowsOfTable(rawTable)
def updateRawTable(username):
    logging.info(paddedLogMessage(f"{username}: Update 'raw_expenses' Table"))
    mainCleaner = MainCleanerExcel(username)
    dataframe, equivalent_columns = mainCleaner.getDataframeAndEqCol()
    dataframe["username"] = username
    myUpdateConversionJson.updateConversionJsonUsingDataframe(dataframe)
    list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
        dataframe, equivalent_columns
    )
    rawTable.insertAllReqs(list_requests)


@updatingByRemovingAllExistingRowsOfTable(repayTable)
def updateRepayementsTable(username):
    logging.info(paddedLogMessage(f"{username}: Update 'reimbursement' Table"))
    rawToRepayement = RawToRepayement(rawTable, repayTable, username)
    response = rawToRepayement.selectRepayementRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToRepayement.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
        dataframe, equivalent_columns
    )
    repayTable.insertAllReqs(list_requests)


# TODO using username
def deleteRepayementsFromRaw(username):
    logging.info(
        paddedLogMessage(f"{username}: Delete 'reimbursement' in 'raw_expenses'")
    )
    rawToRepayement = RawToRepayement(rawTable, repayTable, username)
    response = rawToRepayement.selectRepayementIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    with rawTable:
        rawTable.deleteListRowsId(list_resp)


# TODO using username
def repayRepayements(username):
    logging.info(
        paddedLogMessage(f"{username}: Repay 'reimbursement' in 'raw_expenses'")
    )
    repayRep = RepayPepayements(rawTable, repayTable, username)
    with repayRep:
        response_rep = repayRep.selectRepayementRows()
        dataframe_rep = convertRespToDf.translateResponseSqlToDataframe(
            response_rep, repayTable
        )

        list_ids_pay_orig = repayRep.convertDataframeToListIdsPayOrig(dataframe_rep)
        response_raw = repayRep.selectRowsOfRawWithId(list_ids_pay_orig)
        repayRep.deleteRowsOfRawIds(list_ids_pay_orig)

        dataframe_raw = convertRespToDf.translateResponseSqlToDataframe(
            response_raw, rawTable
        )
        dataframe_cleaned = repayRep.addDfRawAndDfRepayement(
            dataframe_raw, dataframe_rep
        )

        equivalent_columns = convertRespToDf.getEquivalentColumns(rawTable)
        requests_cleaned_rows = convertDfToReq.translateDataframeToInsertRequestSql(
            dataframe_cleaned, equivalent_columns
        )
        # Updating by removing old values, TODO
        list_ids_pay_reimb = repayRep.convertDataframeToListIdsPayOrig(dataframe_rep)
        repayRep.deleteRowsOfRawIds(list_ids_pay_reimb)
        repayRep.insertCleanedRowsReqs(requests_cleaned_rows)


@updatingByRemovingAllExistingRowsOfTable(tripTable)
def updateTripsTable(username):
    logging.info(paddedLogMessage(f"{username}: Update 'trip_expenses'"))
    rawToTrip = RawToTrip(rawTable, tripTable, username)
    response = rawToTrip.selectTripRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToTrip.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
        dataframe, equivalent_columns
    )
    rawToTrip.insertAllReqsInTrip(list_requests)


def deleteTripsFromRaw(username):
    logging.info(
        paddedLogMessage(f"{username}: Delete 'trip_expenses' in 'raw_expenses'")
    )
    rawToTrip = RawToTrip(rawTable, tripTable, username)
    response = rawToTrip.selectTripIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    with rawTable:
        rawTable.deleteListRowsId(list_resp)


@updatingByRemovingAllExistingRowsOfTable(cleanTable)
def updateCleanTable(username):
    logging.info(paddedLogMessage(f"{username}: Update 'clean_expenses'"))
    rawToClean = RawToClean(rawTable, cleanTable, username)
    response = rawToClean.selectAllRemainingRowsInRaw()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToClean.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
        dataframe, equivalent_columns
    )

    logging.info(paddedLogMessage(f"{username}: Adding trip expenses"))
    tripToClean = TripToClean(tripTable, cleanTable, username)
    response = tripToClean.selectAllRemainingRowsInTrip()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, tripTable)
    equivalent_columns = tripToClean.getEquivalentColumns()
    list_requests += convertDfToReq.translateDataframeToInsertRequestSql(
        dataframe, equivalent_columns
    )
    cleanTable.insertAllReqs(list_requests)


# == MAIN == FUNCTION : updates all the tables by removing ALL the older values
def updateAll(username):
    logging.info(paddedLogMessage(""))
    updateExcel(username)

    updateRawTable(username)

    updateRepayementsTable(username)
    deleteRepayementsFromRaw(username)
    repayRepayements(username)

    updateTripsTable(username)
    deleteTripsFromRaw(username)

    updateCleanTable(username)
    logging.info(paddedLogMessage(""))
