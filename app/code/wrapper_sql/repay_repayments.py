import numpy as np


class RepayPepayements:
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
