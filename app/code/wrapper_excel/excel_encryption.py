from cryptography.fernet import Fernet
import io

import pandas as pd
import xlrd

from accessors.access_config import AccessConfig


class ExcelEncryption:
    def __init__(self):
        self.AccessConfig = AccessConfig()
        self.excel_key = self.AccessConfig.getExcelKey()
        self.fernet = Fernet(self.excel_key)

    def writeNewKey(self):
        key = self.fernet.generate_key()
        path_key = self.AccessConfig.ConfigPath.getExcelKeyPath()
        with open(path_key, "wb") as key_file:
            key_file.write(key)

    def encryptAndSaveDataToPath(self, file_data, path_excel):
        encrypted_data = self.encryptData(file_data)
        self.writeBinaryDataTo(encrypted_data, path_excel)

    def getDataFrom(self, path_excel):
        if xlrd.inspect_format(path_excel) == None:
            return self.getDataFromEncryptedFileAtPath(path_excel)
        else:
            return self.readBinaryDataFrom(path_excel)

    def getDataFromEncryptedFileAtPath(self, path_excel):
        with open(path_excel, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return decrypted_data

    def getDataFromEncryptedData(self, encrypted_data):
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return decrypted_data

    def encryptDataframe(self, dataframe, path_excel):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            dataframe.to_excel(writer)
            writer.save()
        buffer.seek(0)
        file_data = buffer.read()
        encrypted_data = self.encryptData(file_data)
        self.writeBinaryDataTo(encrypted_data, path_excel)

    def encryptFile(self, path_excel):
        file_data = self.readBinaryDataFrom(path_excel)
        encrypted_data = self.encryptData(file_data)
        self.writeBinaryDataTo(encrypted_data, path_excel)

    def decryptFile(self, path_excel):
        encrypted_data = self.readBinaryDataFrom(path_excel)
        file_data = self.decryptData(encrypted_data)
        self.writeBinaryDataTo(file_data, path_excel)

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
