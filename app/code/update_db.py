def updatingByRemovingAllExistingRowsOfTable(wrapperTable):
    def updateDecorator(func):
        def inner(*args, **kwargs):
            wrapperTable.dumpTable()
            return func(*args, **kwargs)
        return inner
    return updateDecorator


import config.access_config as access_config
myAccessConfig = access_config.AccessConfig()
config_json = myAccessConfig.getConfig()

import wrapper_excel.access_docs as access_docs
import wrapper_excel.main_cleaner as main_cleaner
import wrapper_excel.cleaner_dataframe as cleaner_dataframe
import wrapper_excel.fill_blanks as fill_blanks
import wrapper_excel.paths_docs as paths_docs
import wrapper_excel.check_conformity as check_conformity

myExcelPath = paths_docs.ExcelPath(config_json)
myDescrToThemePath = paths_docs.DescrToThemePath(config_json)
myTSTAuthorized = paths_docs.ThemesAndSubthemesAuthorized(config_json)

myExcelToDataframe = access_docs.ExcelToDataframe(myExcelPath)
myAccessDescrToTheme = access_docs.AccessDescrToTheme(myDescrToThemePath)
myAccessTSTAuthorized = access_docs.AccessTSTAuthorized(myTSTAuthorized)

myCleanerDataframe = cleaner_dataframe.CleanerDataframe()
myIntelligentFill = fill_blanks.IntelligentFill(myAccessDescrToTheme)
myReviewerDataframe = check_conformity.ReviewerDataframe(myAccessTSTAuthorized)
mainCleaner = main_cleaner.MainCleanerExcel(myExcelToDataframe, myCleanerDataframe, myIntelligentFill, myReviewerDataframe)

myUpdateConversionJson = fill_blanks.UpdateConversionJson(myAccessDescrToTheme)




import wrapper_sql.wrapper_sql as wrapper_sql
import wrapper_sql.dataframe_to_request_sql as dataframe_to_request_sql
import wrapper_sql.table_to_other_table as table_to_other_table
import wrapper_sql.repay_repayments as repay_repayments

convertDfToReq = dataframe_to_request_sql.DataframeToSql()
convertRespToDf = wrapper_sql.ResponseSqlToDataframe()
convertRespToList = wrapper_sql.ResponseSqlToList()

rawTable = wrapper_sql.WrapperOfTable("depenses_brutes", config_json)
tripTable = wrapper_sql.WrapperOfTable("depenses_voyages", config_json)
repayTable = wrapper_sql.WrapperOfTable("remboursements", config_json)
cleanTable = wrapper_sql.WrapperOfTable("depenses_propres", config_json)

rawToRepayement = table_to_other_table.RawToRepayement(rawTable, repayTable)
rawToTrip = table_to_other_table.RawToTrip(rawTable, tripTable)
rawToClean = table_to_other_table.RawToClean(rawTable, cleanTable)
tripToClean = table_to_other_table.TripToClean(tripTable, cleanTable)

repayRep = repay_repayments.RepayPepayements(rawTable, repayTable)





@updatingByRemovingAllExistingRowsOfTable(rawTable)
def updateRawTable():
    print("--- Update 'depenses_brutes' Table ---")
    mainCleaner.updateExcel()
    dataframe, equivalent_columns = mainCleaner.getDataframeAndEqCol()
    myUpdateConversionJson.updateConversionJsonUsingDataframe(dataframe)
    list_requests = convertDfToReq.translateDataframeToRequestSql(dataframe, equivalent_columns)
    rawTable.insertAllReqs(list_requests)
    #return list_requests



@updatingByRemovingAllExistingRowsOfTable(repayTable)
def updateRepayementsTable():
    print("--- Update 'remboursement' Table ---")
    response = rawToRepayement.selectRepayementRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToRepayement.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(dataframe, equivalent_columns)
    repayTable.insertAllReqs(list_requests)
    #return list_requests

def deleteRepayementsFromRaw():
    print("--- Delete 'remboursement' in 'depenses_brutes' ---")
    response = rawToRepayement.selectRepayementIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    rawTable.deleteListRowsId(list_resp)

def repayRepayements():
    print("--- Repay 'remboursement' in 'depenses_brutes' ---")
    response_rep = repayRep.selectRepayementRows()
    dataframe_rep = convertRespToDf.translateResponseSqlToDataframe(response_rep, repayTable)
    
    list_ids_pay_orig = repayRep.convertDataframeToListIdsPayOrig(dataframe_rep)
    response_raw = repayRep.selectRowsOfRawWhereIds(list_ids_pay_orig)
    repayRep.deleteRowsOfRawWhereIds(list_ids_pay_orig)
    
    dataframe_raw = convertRespToDf.translateResponseSqlToDataframe(response_raw, rawTable)
    dataframe_cleaned = repayRep.addDfRawAndDfRepayement(dataframe_raw, dataframe_rep)
    
    equivalent_columns = convertRespToDf.getEquivalentColumns(rawTable)
    requests_cleaned_rows = convertDfToReq.translateDataframeToRequestSql(dataframe_cleaned, equivalent_columns)
    repayRep.insertCleanedRowsReqs(requests_cleaned_rows)



@updatingByRemovingAllExistingRowsOfTable(tripTable)
def updateTripsTable():
    print("--- Update 'depenses_voyages' ---")
    response = rawToTrip.selectTripRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToTrip.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(dataframe, equivalent_columns)
    tripTable.insertAllReqs(list_requests)
    #return list_requests

def deleteTripsFromRaw():
    print("--- Delete 'depenses_voyages' in 'depenses_brutes' ---")
    response = rawToTrip.selectTripIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    rawTable.deleteListRowsId(list_resp)



@updatingByRemovingAllExistingRowsOfTable(cleanTable)
def updateCleanTable():
    print("--- Update 'depenses_propres' ---")
    response = rawToClean.selectAllRemainingRowsInRaw()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToClean.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(dataframe, equivalent_columns)
    
    print("--- Adding trip expenses ---")
    response = tripToClean.selectAllRemainingRowsInTrip()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, tripTable)
    equivalent_columns = tripToClean.getEquivalentColumns()
    list_requests += convertDfToReq.translateDataframeToRequestSql(dataframe, equivalent_columns)
    cleanTable.insertAllReqs(list_requests)
    #return list_requests



# main
def updateAll():
    updateRawTable()

    updateRepayementsTable()
    deleteRepayementsFromRaw()
    repayRepayements()

    updateTripsTable()
    deleteTripsFromRaw()

    updateCleanTable()