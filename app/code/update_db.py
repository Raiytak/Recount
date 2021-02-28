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

import accessors.paths_docs as paths_docs
myExcelPath = paths_docs.ExcelPath(config_json)
myDescrToThemePath = paths_docs.DescrToThemePath(config_json)
myCatThemeAuthPath = paths_docs.CategoryAndThemeAuthorizedPath(config_json)

import accessors.access_docs as access_docs
myAccessDescrToTheme = access_docs.AccessDescrToTheme(myDescrToThemePath)
myAccessCTAuthorized = access_docs.AccessCTAuthorized(myCatThemeAuthPath)
myAccessExcel = access_docs.AccessExcel(myExcelPath)



import wrapper_excel.convert_excel_to_df as convert_excel_to_df
import wrapper_excel.main_cleaner as main_cleaner
import wrapper_excel.cleaner_dataframe as cleaner_dataframe
import wrapper_excel.fill_blanks as fill_blanks
import wrapper_excel.check_conformity as check_conformity


myExcelToDataframe = convert_excel_to_df.ExcelToDataframe(myAccessExcel)
myCleanerDataframe = cleaner_dataframe.CleanerDataframe()
myIntelligentFill = fill_blanks.IntelligentFill(myAccessDescrToTheme)
myReviewerDataframe = check_conformity.ReviewerDataframe(myAccessCTAuthorized)
mainCleaner = main_cleaner.MainCleanerExcel(myExcelToDataframe, myCleanerDataframe, myIntelligentFill, myReviewerDataframe)

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





@updatingByRemovingAllExistingRowsOfTable(rawTable)
def updateRawTable():
    print("--- Update 'raw_expenses' Table ---")
    mainCleaner.updateExcel()
    dataframe, equivalent_columns = mainCleaner.getDataframeAndEqCol()
    myUpdateConversionJson.updateConversionJsonUsingDataframe(dataframe)
    list_requests = convertDfToReq.translateDataframeToRequestSql(dataframe, equivalent_columns)
    rawTable.insertAllReqs(list_requests)



@updatingByRemovingAllExistingRowsOfTable(repayTable)
def updateRepayementsTable():
    print("--- Update 'reimbursement' Table ---")
    response = rawToRepayement.selectRepayementRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)    
    equivalent_columns = rawToRepayement.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(dataframe, equivalent_columns)
    repayTable.insertAllReqs(list_requests)

def deleteRepayementsFromRaw():
    print("--- Delete 'reimbursement' in 'raw_expenses' ---")
    response = rawToRepayement.selectRepayementIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    rawTable.deleteListRowsId(list_resp)

def repayRepayements():
    print("--- Repay 'reimbursement' in 'raw_expenses' ---")
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
    print("--- Update 'trip_expenses' ---")
    response = rawToTrip.selectTripRows()
    dataframe = convertRespToDf.translateResponseSqlToDataframe(response, rawTable)
    equivalent_columns = rawToTrip.getEquivalentColumns()
    list_requests = convertDfToReq.translateDataframeToRequestSql(dataframe, equivalent_columns)
    tripTable.insertAllReqs(list_requests)

def deleteTripsFromRaw():
    print("--- Delete 'trip_expenses' in 'raw_expenses' ---")
    response = rawToTrip.selectTripIds()
    list_resp = convertRespToList.translateResponseSqlToList(response)
    rawTable.deleteListRowsId(list_resp)



@updatingByRemovingAllExistingRowsOfTable(cleanTable)
def updateCleanTable():
    print("--- Update 'clean_expenses' ---")
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



# == MAIN == FUNCTION : updates all the tables by removing ALL the older values
def updateAll():
    updateRawTable()

    updateRepayementsTable()
    deleteRepayementsFromRaw()
    repayRepayements()

    updateTripsTable()
    deleteTripsFromRaw()

    updateCleanTable()