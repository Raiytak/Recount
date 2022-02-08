# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
TODO
"""

import pandas as pd

import access


class ExcelToDataframe:
    """Wrapper to get the user data from its excel, and the SQL equivalent columns"""

    def __init__(self, username=None):
        self.access_user_file = access.AccessUserFiles(username)

    def getDataframe(self):
        excel_data = self.access_user_file.excel()
        return pd.read_excel(excel_data)  # To remove id col: , index_col=[0]

    def getEquivalentColumns(self):
        """Returns a dict as follow:
        column excel : [column sql]"""

        equivalent_columns = {
            "username": "username",
            "ID": "ID",
            "Date": "date",
            "Expenses": "amount",
            "Category": "category",
            "Theme": "theme",
            "Trip": "trip",
            "Type": "payment_method",
            "Company": "company",
            "Description": "description",
        }
        return equivalent_columns
