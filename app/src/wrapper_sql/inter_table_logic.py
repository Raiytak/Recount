# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Logic used to update the different tables when an update_all from update_data
is called (except raw_expenses: table raw_repayement is filled first
using the cleaned_excel and will be used to fill the others).
"""

import numpy as np


class RawToRepayement:
    """Select the repayement rows of raw_expenses and add them to the repayement table"""
    def __init__(self, rawTable, repayTable, username):
        self.rawTable = rawTable
        self.repayTable = repayTable
        self.username = username

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectRepayementRows(self):
        request = (
            "SELECT * FROM & where category = 'reimbursement' AND username = '"
            + self.username
            + "'"
        )
        response = self.rawTable.select(request)
        return response

    def insertAllReqs(self, requests):
        for req in requests:
            self.repayTable.insert(req)

    def selectRepayementIds(self):
        request = "SELECT ID FROM &"
        response = self.repayTable.select(request)
        return response

    def deleteRepayementRowsInRaw(self, requests):
        for req in requests:
            self.rawTable.deleteRowId(req)

    def getEquivalentColumns(self):
        equivalent_columns = {
            "username": ["username"],
            "ID": ["ID"],
            "theme": ["ID_pay_orig"],
            "date": ["date"],
            "amount": ["amount"],
        }
        return equivalent_columns


class RawToTrip:
    """Select the trip rows of raw_expenses and add them to the trip table"""
    def __init__(self, rawTable, tripTable, username):
        self.rawTable = rawTable
        self.tripTable = tripTable
        self.username = username

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectTripRows(self):
        request = (
            "SELECT * FROM & WHERE trip IS NOT NULL AND username = '"
            + self.username
            + "'"
        )
        response = self.rawTable.select(request)
        return response

    def insertAllReqs(self, requests):
        for req in requests:
            self.tripTable.insert(req)

    def selectTripIds(self):
        request = "SELECT ID FROM & WHERE username = '" + self.username + "'"
        response = self.tripTable.select(request)
        return response

    def deleteTripRowsInRaw(self, requests):
        for req in requests:
            self.rawTable.deleteRowId(req)

    def getEquivalentColumns(self):
        # "origin":["destination"]
        columns = self.rawTable.getNameColumns()
        equivalent_columns = {col: [col] for col in columns}
        return equivalent_columns

    def dumpTripTableForUser(self, username):
        self.tripTable.dumpTableForUser(username)

    def insertAllReqsInTrip(self, list_request_sql):
        self.tripTable.insertAllReqs(list_request_sql)


class RawToClean:
    """Select the trip rows of raw_expenses and add them to the clean table"""
    def __init__(self, rawTable, cleanTable, username):
        self.rawTable = rawTable
        self.cleanTable = cleanTable
        self.username = username

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectAllRemainingRowsInRaw(self):
        request = "SELECT * FROM &"
        response = self.rawTable.select(request)
        return response

    def insertAllReqs(self, requests):
        for req in requests:
            self.cleanTable.insert(req)

    def getEquivalentColumns(self):
        # "origin":["destination"]
        columns = self.cleanTable.getNameColumns()
        equivalent_columns = {col: [col] for col in columns}
        return equivalent_columns


class TripToClean:
    """Select the trip rows of trip and add them to the clean table"""
    def __init__(self, tripTable, cleanTable, username):
        self.tripTable = tripTable
        self.cleanTable = cleanTable
        self.username = username

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectAllRemainingRowsInTrip(self):
        request = "SELECT * FROM & WHERE username = '" + self.username + "'"
        response = self.tripTable.select(request)
        return response

    def insertAllReqs(self, requests):
        self.cleanTable.dumpTable()
        for req in requests:
            self.cleanTable.insert(req)

    def insertAllReqs(self, requests):
        for req in requests:
            self.cleanTable.insert(req)

    def getEquivalentColumns(self):
        # "origin":["destination"]
        columns = self.cleanTable.getNameColumns()
        equivalent_columns = {col: [col] for col in columns}
        return equivalent_columns


class RepayPepayements:
    """Create and manage a connection to the MySQL database"""
    def __init__(self, rawTable, repayTbale, username):
        self.rawTable = rawTable
        self.repayTable = repayTbale
        self.username = username

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectRepayementRows(self):
        request = "SELECT * FROM & WHERE username = '" + self.username + "'"
        response = self.repayTable.select(request)
        return response

    def selectRowsOfRawWithId(self, list_ids_pay_orig):
        return self.rawTable.selectListRowId(list_ids_pay_orig)

    def selectRepayementIds(self):
        request = "SELECT ID FROM & WHERE username = '" + self.username + "'"
        response = self.repayTable.select(request)
        return response

    def deleteRowsOfRawIds(self, list_ids_pay_orig):
        for id in list_ids_pay_orig:
            self.rawTable.deleteRowId(id)

    def deleteRepayementRowsInRaw(self, requests):
        for req in requests:
            self.rawTable.deleteRowId(req)

    def insertRepayementReqs(self, requests):
        self.repayTable.dumpTable()
        for req in requests:
            self.repayTable.insert(req)

    def insertCleanedRowsReqs(self, requests):
        for req in requests:
            self.rawTable.insert(req)

    def convertDataframeToListIdsPayOrig(self, dataframe_rep):
        list_ids_pay_orig = list(dataframe_rep["ID_pay_orig"])
        return list_ids_pay_orig

    def convertDataframeToListIdsPayReimbursed(self, dataframe_rep):
        list_ids_pay_orig = list(dataframe_rep["ID"])
        return list_ids_pay_orig

    def addDfRawAndDfRepayement(self, dataframe_raw, dataframe_rep):
        dataframe_raw = dataframe_raw.sort_values(by="ID")
        dataframe_rep = dataframe_rep.sort_values(by="ID_pay_orig")
        sum_expense = np.around(dataframe_raw["amount"] + dataframe_rep["amount"], 2)
        dataframe_raw["amount"] = sum_expense

        dataframe_clean = dataframe_raw.loc[dataframe_raw["amount"] > 1]

        return dataframe_clean

    def getEquivalentColumns(self):
        # "origin":["destination"]
        equivalent_columns = {
            "ID": ["ID"],
            "theme": ["ID_pay_orig"],
            "date": ["date"],
            "amount": ["amount"],
        }
        return equivalent_columns
