from cryptography.fernet import Fernet
import pickle
import io

import pandas as pd

from accessors.access_config import AccessConfig


class ExcelEncryption:
    def __init__(self):
        self.AccessConfig = AccessConfig()
        self.excel_key = self.AccessConfig.getExcelKey()
        self.fernet = Fernet(self.excel_key)

    def writeNewKey(self):
        """
        Generates a key and save it into a file
        """
        key = self.fernet.generate_key()
        path_key = self.AccessConfig.ConfigPath.getExcelKeyPath()
        with open(path_key, "wb") as key_file:
            key_file.write(key)

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
        encrypted_data = self.fernet.encrypt(file_data)
        self.writeBinaryDataTo(path_excel, encrypted_data)

    def encryptFile(self, path_excel):
        file_data = self.readBinaryDataFrom(path_excel)
        encrypted_data = self.fernet.encrypt(file_data)
        self.writeBinaryDataTo(path_excel, encrypted_data)

    def decryptFile(self, path_excel):
        encrypted_data = self.readBinaryDataFrom(path_excel)
        file_data = self.fernet.decrypt(encrypted_data)
        self.writeBinaryDataTo(path_excel, file_data)

    def readBinaryDataFrom(self, file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
        return file_data

    def writeBinaryDataTo(self, file_path, file_data):
        with open(file_path, "wb") as file:
            file_data = file.write(file_data)
