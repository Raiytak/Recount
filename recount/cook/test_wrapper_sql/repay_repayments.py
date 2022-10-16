import numpy as np
import pandas as pd


class RepayPepayements:
    def __init__(self, wrapper_table_raw, wrapper_table_repayement):
        self.table_raw = wrapper_table_raw
        self.table_rep = wrapper_table_repayement
        self.name = "repayRepayements"

    def selectRepayementRows(self):
        request = "SELECT * FROM &"
        response = self.table_rep.select(request)
        return response

    def selectRowsOfRawWhereIds(self, list_ids_pay_orig):
        list_rows = []
        for id in list_ids_pay_orig:
            list_rows.append(self.table_raw.selectRowId(id)[0])
        return tuple(list_rows)

    def selectRepayementIds(self):
        request = "SELECT ID FROM &"
        response = self.table_rep.select(request)
        return response

    def deleteRowsOfRawWhereIds(self, list_ids_pay_orig):
        for id in list_ids_pay_orig:
            self.table_raw.deleteRowId(id)

    def deleteRepayementRowsInRaw(self, requests):
        for req in requests:
            self.table_raw.deleteRowId(req)

    def insertRepayementReqs(self, requests):
        self.table_rep.dumpTable()
        for req in requests:
            self.table_rep.insert(req)

    def insertCleanedRowsReqs(self, requests):
        for req in requests:
            self.table_raw.insert(req)

    def convertDataframeToListIdsPayOrig(self, dataframe_rep):
        list_ids_pay_orig = list(dataframe_rep["ID_pay_orig"])
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
