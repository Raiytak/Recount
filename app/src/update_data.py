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

from genericpath import exists
import logging
from logs.logs import paddedLogMessage
from accessors.access_files import AccessConfig
from accessors.access_files import AccessUserFiles


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
from wrapper_sql.df_sql_conversion import (
    DataframeToSql,
    ResponseSqlToDataframe,
    ResponseSqlToList,
)
from wrapper_sql.inter_table_logic import (
    RawToRepayement,
    RawToTrip,
    RawToClean,
    TripToClean,
    RepayPepayements,
)

convertDfToReq = DataframeToSql()
convertRespToDf = ResponseSqlToDataframe()
convertRespToList = ResponseSqlToList()

rawTable = WrapperOfTable("raw_expenses", db_config)
tripTable = WrapperOfTable("trip_expenses", db_config)
repayTable = WrapperOfTable("reimbursement", db_config)
cleanTable = WrapperOfTable("clean_expenses", db_config)


def updateExcel(username):
    """Copy the imported excel (if exists then remove it),
    create a new excel that is used for cleaning the data that will then be uploaded on MySQL."""
    logging.info(paddedLogMessage(f"{username}: Update excel files"))
    mainCleaner = MainCleanerExcel(username)
    try:
        mainCleaner.updateExcel()
    except Exception as exp:
        logging.info(paddedLogMessage(f"The excel files created errors: {exp}"))
        return False
    return True


@updatingByRemovingAllExistingRowsOfTable(rawTable)
def updateRawTable(username):
    """Convert the cleaned excel to MySQL, then remove the cleaned excel (redundant data)"""
    logging.info(paddedLogMessage(f"{username}: Update 'raw_expenses' Table"))
    mainCleaner = MainCleanerExcel(username)
    dataframe, equivalent_columns = mainCleaner.getDataframeAndEqCol()
    dataframe["username"] = username
    myUpdateConversionJson.updateConversionJsonUsingDataframe(dataframe)
    list_requests = convertDfToReq.translateDataframeToInsertRequestSql(
        dataframe, equivalent_columns
    )
    rawTable.insertAllReqs(list_requests)
    # Remove all excels except the raw one
    removeAllExcelsExceptRawForUser(username)


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


# TODO verify use username
def deleteRepayementsFromRaw(username):
    logging.info(
        paddedLogMessage(f"{username}: Delete 'reimbursement' in 'raw_expenses'")
    )
    rawToRepayement = RawToRepayement(rawTable, repayTable, username)
    response = rawToRepayement.selectRepayementIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    with rawTable:
        rawTable.deleteListRowsId(list_resp)


# TODO verify use username
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


def updateSqlDb(username):
    updateRawTable(username)

    updateRepayementsTable(username)
    deleteRepayementsFromRaw(username)
    repayRepayements(username)

    updateTripsTable(username)
    deleteTripsFromRaw(username)

    updateCleanTable(username)
    logging.info(paddedLogMessage(""))


def removeAllDataForUser(username):
    removeAllExcelsForUser(username)
    removeAllSqlDataForUser(username)


def removeAllSqlDataForUser(username):
    rawTable.dumpTableForUser(username)
    repayTable.dumpTableForUser(username)
    tripTable.dumpTableForUser(username)
    cleanTable.dumpTableForUser(username)


def removeAllExcelsForUser(username):
    myAccessUserFiles = AccessUserFiles(username)
    myAccessUserFiles.removeExcelsOfUser()


def removeAllExcelsExceptRawForUser(username):
    myAccessUserFiles = AccessUserFiles(username)
    myAccessUserFiles.removeExcelsExceptRawOfUser()


def updateAll(username):
    """Updates all the tables of the given user.
    For now it removes ALL the older values."""
    # TODO: improve remove ALL -> update values
    # TODO: use cache
    # TODO: use data encryption
    logging.info(paddedLogMessage(""))
    sql_is_to_update = updateExcel(username)
    if sql_is_to_update == True:
        updateSqlDb(username)
