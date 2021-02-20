import numpy as np
import pandas as pd



class RawToRepayement():
    def __init__(self, wrapper_table_raw, wrapper_table_repayement):
        self.table_raw = wrapper_table_raw
        self.table_rep = wrapper_table_repayement
        self.name = "rawToRepayement"
        
    def selectRepayementRows(self):
        request = "SELECT * FROM & where category = 'reimbursement'"
        response = self.table_raw.select(request)
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
            self.table_raw.deleteRowId(req)
            
    
    def getEquivalentColumns(self):
        equivalent_columns = {"ID":["ID"], "theme":["ID_pay_orig"], "date":["date"], "amount":["amount"]}
        return equivalent_columns


class RawToTrip():
    def __init__(self, wrapper_table_raw, wrapper_table_trip):
        self.table_raw = wrapper_table_raw
        self.table_trip = wrapper_table_trip
        self.name = "rawToTrip"
        
    def selectTripRows(self):
        request = "SELECT * FROM & where trip IS NOT NULL"
        response = self.table_raw.select(request)
        return response
    
    def insertAllReqs(self, requests):
        for req in requests:
            self.table_trip.insert(req)
            
    def selectTripIds(self):
        request = "SELECT ID FROM &"
        response = self.table_trip.select(request)
        return response
        
    def deleteTripRowsInRaw(self, requests):
        for req in requests:
            self.table_raw.deleteRowId(req)
            
            
    def getEquivalentColumns(self):
        columns = self.table_raw.getNameColumns()
        equivalent_columns = {col:[col] for col in columns}
        return equivalent_columns



class RawToClean():
    def __init__(self, wrapper_table_raw, wrapper_table_clean):
        self.table_raw = wrapper_table_raw
        self.table_clean = wrapper_table_clean
        self.name = "rawToClean"
        
    def selectAllRemainingRowsInRaw(self):
        request = "SELECT * FROM &"
        response = self.table_raw.select(request)
        return response
    
    def insertAllReqs(self, requests):
        for req in requests:
            self.table_clean.insert(req)
            
    def getEquivalentColumns(self):
        columns = self.table_clean.getNameColumns()
        equivalent_columns = {col:[col] for col in columns}
        return equivalent_columns
    
    
    
class TripToClean():
    def __init__(self, wrapper_table_trip, wrapper_table_clean):
        self.table_trip = wrapper_table_trip
        self.table_clean = wrapper_table_clean
        self.name = "tripToClean"
        
    def selectAllRemainingRowsInTrip(self):
        request = "SELECT * FROM &"
        response = self.table_trip.select(request)
        return response
    
    def insertAllReqs(self, requests):
        self.table_clean.dumpTable()
        for req in requests:
            self.table_clean.insert(req)
            
    def insertAllReqs(self, requests):
        for req in requests:
            self.table_clean.insert(req)
            
            
    def getEquivalentColumns(self):
        columns = self.table_clean.getNameColumns()
        equivalent_columns = {col:[col] for col in columns}
        return equivalent_columns
    


    
    

    
    