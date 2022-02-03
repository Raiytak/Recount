# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
This file is the encryption layer protecting SQL database.
"""

import re

from access_files import AccessConfig


class SqlEncryption:
    """Encryption logic of the SQL exchanges."""

    def __init__(self):
        self.AccessConfig = AccessConfig()
        sql_key = self.AccessConfig.getDataSqlKey()
        self.list_columns_to_left_unchanged = [
            "ID",
            "_id",
            "date",
            "username",
            "payment_method",
        ]
        super().__init__(sql_key)

    def encryptInsertion(self, insert_request):
        self.assureIsInsertionRequest(insert_request)
        list_columns, list_values = self.getColumnsAndValues(insert_request)
        dict_encryption = self.encryptValuesOfColumnsUsingAES(list_columns, list_values)
        request_encrypted = self.replaceRequestByEncryptedValues(
            insert_request, dict_encryption
        )
        return request_encrypted

    def encryptManuallyInsertion(self, insert_request):
        self.assureIsInsertionRequest(insert_request)
        list_columns, list_values = self.getColumnsAndValues(insert_request)
        dict_encryption = self.encryptValuesOfColumnsUsingCryptocode(
            list_columns, list_values
        )
        request_encrypted = self.replaceRequestByEncryptedValues(
            insert_request, dict_encryption
        )
        return request_encrypted

    def assureIsInsertionRequest(self, insert_request):
        if ("INSERT INTO" in insert_request) == False:
            raise AttributeError(f"Not an insertion request: {insert_request}")

    def getColumnsAndValues(self, insert_request):
        tuples = re.findall("\(.*?\)", insert_request)

        columns = tuples[0][1:-1]
        list_columns = re.split(", ", columns)

        values = tuples[1][1:-1]
        values = re.sub("'", "", values)
        list_values = re.split(", ", values)

        return list_columns, list_values

    def encryptValuesOfColumnsUsingAES(self, list_columns, list_values):
        dict_replacement = {}
        for column in list_columns:
            i_col = list_columns.index(column)
            value_unchanged = list_values[i_col]
            if value_unchanged == "nan":
                dict_replacement[value_unchanged] = "NULL"
            elif column not in self.list_columns_to_left_unchanged:
                value_encrypted = self.encryptValueUsingAES(value_unchanged)
                dict_replacement[value_unchanged] = value_encrypted
            else:
                dict_replacement[value_unchanged] = value_unchanged
        return dict_replacement

    def encryptValuesOfColumnsUsingCryptocode(self, list_columns, list_values):
        dict_replacement = {}
        for column in list_columns:
            i_col = list_columns.index(column)
            value_unchanged = list_values[i_col]
            if (column not in self.list_columns_to_left_unchanged) and (
                value_unchanged != "nan"
            ):
                value_encrypted = self.encryptValueUsingCryptocode(value_unchanged)
                dict_replacement[value_unchanged] = value_encrypted
            else:
                dict_replacement[value_unchanged] = value_unchanged
        return dict_replacement

    def encryptValueUsingAES(self, value):
        encrypted_value = "AES_ENCRYPT('" + value + "', " + self.key + ")"
        return encrypted_value

    def decryptValueUsingAES(self, encrypted_value):
        value = "AES_DECRYPT('" + encrypted_value + "', " + self.key + ")"
        return value

    def encryptValueUsingCryptocode(self, value):
        # return cryptocode.encrypt(value, self.key)
        return value

    def decryptValueUsingCryptocode(self, value):
        # return cryptocode.decrypt(value, self.key)
        return value

    def replaceRequestByEncryptedValues(self, request, dict_values_encrypted):
        try:
            for value in dict_values_encrypted.keys():
                encrypted = dict_values_encrypted[value]
                request = re.sub(value, encrypted, request)
        except re.error:
            logging.debug(f"value: {value}\nrequest:{request}")
        return request
