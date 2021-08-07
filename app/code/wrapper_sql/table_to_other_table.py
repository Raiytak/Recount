class RawToRepayement:
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
