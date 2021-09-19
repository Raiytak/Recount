import logging
from cryptography.fernet import Fernet
import io

import pandas as pd
import xlrd

import re

# import cryptocode

from accessors.access_config import AccessConfig


class DataEncryption:
    def __init__(self, key):
        self.key = key
        if type(self.key) == bytes:
            try:
                self.fernet = Fernet(self.key)
            except ValueError:
                pass

    def writeNewKey(self, path_key):
        key = self.fernet.generate_key()
        with open(path_key, "wb") as key_file:
            key_file.write(key)

    def encryptAndSaveDataToPath(self, file_data, file_path):
        encrypted_data = self.encryptData(file_data)
        self.writeBinaryDataTo(encrypted_data, file_path)

    def getDataFromEncryptedFileAtPath(self, file_path):
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return decrypted_data

    def getDataFromEncryptedData(self, encrypted_data):
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return decrypted_data

    def encryptFile(self, file_path):
        file_data = self.readBinaryDataFrom(file_path)
        encrypted_data = self.encryptData(file_data)
        self.writeBinaryDataTo(encrypted_data, file_path)

    def decryptFile(self, file_path):
        encrypted_data = self.readBinaryDataFrom(file_path)
        file_data = self.decryptData(encrypted_data)
        self.writeBinaryDataTo(file_data, file_path)

    def readBinaryDataFrom(self, file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
        return file_data

    def writeBinaryDataTo(self, file_data, file_path):
        with open(file_path, "wb") as file:
            file_data = file.write(file_data)

    def writeStringDataTo(self, file_data, file_path):
        with open(file_path, "w") as file:
            file_data = file.write(file_data)

    def encryptData(self, file_data):
        encrypted_data = self.fernet.encrypt(file_data)
        return encrypted_data

    def decryptData(self, encrypted_data):
        file_data = self.fernet.decrypt(encrypted_data)
        return file_data


class ExcelEncryption(DataEncryption):
    def __init__(self):
        self.AccessConfig = AccessConfig()
        excel_key = self.AccessConfig.getExcelKey()
        super().__init__(excel_key)

    def getDataFrom(self, path_excel):
        if xlrd.inspect_format(path_excel) == None:
            return self.getDataFromEncryptedFileAtPath(path_excel)
        else:
            return self.readBinaryDataFrom(path_excel)

    def encryptDataframe(self, dataframe, path_excel):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            dataframe.to_excel(writer)
            writer.save()
        buffer.seek(0)
        file_data = buffer.read()
        encrypted_data = self.encryptData(file_data)
        self.writeBinaryDataTo(encrypted_data, path_excel)


class SqlEncryption(DataEncryption):
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
