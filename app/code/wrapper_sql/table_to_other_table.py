import numpy as np
import pandas as pd


class RawToRepayement:
    def __init__(self, WrapperTableRaw, wrapper_table_repayement):
        self.TableRaw = WrapperTableRaw
        self.table_rep = wrapper_table_repayement
        self.name = "rawToRepayement"

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectRepayementRows(self):
        request = "SELECT * FROM & where category = 'reimbursement'"
        response = self.TableRaw.select(request)
        return response

    def insertAllReqs(self, requests):
        for req in requests:
            self.table_rep.insert(req)

    def selectRepayementIds(self):
        request = "SELECT ID FROM &"
        response = self.table_rep.select(request)
        return response

    def deleteRepayementRowsInRaw(self, requests):
        for req in requests:
            self.TableRaw.deleteRowId(req)

    def getEquivalentColumns(self):
        # "origin":["destination"]
        equivalent_columns = {
            "username": ["username"],
            "ID": ["ID"],
            "theme": ["ID_pay_orig"],
            "date": ["date"],
            "amount": ["amount"],
        }
        return equivalent_columns


class RawToTrip:
    def __init__(self, WrapperTableRaw, WrapperTableTrip):
        self.TableRaw = WrapperTableRaw
        self.TableTrip = WrapperTableTrip
        self.name = "rawToTrip"

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectTripRows(self):
        request = "SELECT * FROM & where trip IS NOT NULL"
        response = self.TableRaw.select(request)
        return response

    def insertAllReqs(self, requests):
        for req in requests:
            self.TableTrip.insert(req)

    def selectTripIds(self):
        request = "SELECT ID FROM &"
        response = self.TableTrip.select(request)
        return response

    def deleteTripRowsInRaw(self, requests):
        for req in requests:
            self.TableRaw.deleteRowId(req)

    def getEquivalentColumns(self):
        # "origin":["destination"]
        columns = self.TableRaw.getNameColumns()
        equivalent_columns = {col: [col] for col in columns}
        return equivalent_columns

    def dumpTripTableForUser(self, username):
        self.TableTrip.dumpTableForUser(username)

    def insertAllReqsInTrip(self, list_request_sql):
        self.TableTrip.insertAllReqs(list_request_sql)


class RawToClean:
    def __init__(self, WrapperTableRaw, WrapperTableClean):
        self.TableRaw = WrapperTableRaw
        self.table_clean = WrapperTableClean
        self.name = "rawToClean"

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectAllRemainingRowsInRaw(self):
        request = "SELECT * FROM &"
        response = self.TableRaw.select(request)
        return response

    def insertAllReqs(self, requests):
        for req in requests:
            self.table_clean.insert(req)

    def getEquivalentColumns(self):
        # "origin":["destination"]
        columns = self.table_clean.getNameColumns()
        equivalent_columns = {col: [col] for col in columns}
        return equivalent_columns


class TripToClean:
    def __init__(self, WrapperTableTrip, WrapperTableClean):
        self.TableTrip = WrapperTableTrip
        self.table_clean = WrapperTableClean
        self.name = "tripToClean"

    def __enter__(self):
        pass
        # self.myConnection, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # self._end_connection()

    def selectAllRemainingRowsInTrip(self):
        request = "SELECT * FROM &"
        response = self.TableTrip.select(request)
        return response

    def insertAllReqs(self, requests):
        self.table_clean.dumpTable()
        for req in requests:
            self.table_clean.insert(req)

    def insertAllReqs(self, requests):
        for req in requests:
            self.table_clean.insert(req)

    def getEquivalentColumns(self):
        # "origin":["destination"]
        columns = self.table_clean.getNameColumns()
        equivalent_columns = {col: [col] for col in columns}
        return equivalent_columns
