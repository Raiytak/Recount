import os
import io
import base64
import csv
import pandas as pd

from wrapper_excel.convert_excel_to_df import ExcelToDataframe


class ImportExcelFileSaver:
    def __init__(self, update_db):
        self.ExcelToDataframe = ExcelToDataframe()
        self.AccessExcel = self.ExcelToDataframe.AccessExcel
        self.ExcelPaths = self.ExcelToDataframe.ExcelPaths

        self.update_db = update_db

    def getDataframe(self):
        return self.ExcelToDataframe.getDataframeOfRawExcel()

    def getContentTypeAndStringOfImportedFile(self, file_imported):
        content_type, content_string_encoded = file_imported.split(",")
        return content_type, content_string_encoded

    def getTypeAndDecodeImportedFile(
        self, content_type_encoded, content_string_encoded
    ):
        content_string_base64 = base64.b64decode(content_string_encoded)
        if ("xml" in content_type_encoded) or ("xls" in content_type_encoded):
            content_decoded = io.BytesIO(content_string_base64)
            content_type = "xlsx"
        else:
            content_type = content_type_encoded
        return content_type, content_decoded

    def decodeImportedFile(self, file_imported):
        (
            content_type_encoded,
            content_string_encoded,
        ) = self.getContentTypeAndStringOfImportedFile(file_imported)
        content_type, content_decoded = self.getTypeAndDecodeImportedFile(
            content_type_encoded, content_string_encoded
        )
        return content_type, content_decoded

    def saveContentStringIntoXlsxFile(self, content_type, content_decoded):
        path_file = self.ExcelPaths.rawCopiedExcelPath()
        if content_type == "xlsx":
            with open(path_file, "wb") as f:
                f.write(content_decoded.read())

    def checkIsAXlsxFile(self, content_type):
        if content_type != "xlsx":
            raise TypeError

    def updateDbs(self):
        self.update_db.updateAll()

    def saveImportedFile(self, file_imported):
        # If there is nothing to save, the function stops
        if file_imported != None:
            try:
                content_type, content_decoded = self.decodeImportedFile(file_imported)
                self.checkIsAXlsxFile(content_type)
                self.saveContentStringIntoXlsxFile(content_type, content_decoded)
                return "File imported"

            except TypeError:
                # print(" >>> The file imported is not a '.xlsx' file <<< ")
                return " >>> The file imported is not a '.xlsx' file <<< "
        return ""

    # def saveTemporaryRawExcelFromInputData(self, data_excel):
    def saveNotebookDataTorawExcel(self, data_excel):
        # If there is nothing to save, the function stops
        try:
            dataframe = pd.DataFrame(data_excel)
            dataframe.to_excel(self.ExcelPaths.rawCopiedExcelPath(), index=False)
        except Exception:
            # print(" >>> An error has occcured during the update.<<<\n >>> Please check the values you have inserted <<<")
            return " >>> An error has occcured during the update. Please check the values you have inserted <<<"

        return "Update done"

    def translateDataframeToNotebookData(self, dataframe):
        data_for_output = dataframe.to_dict("records")
        return data_for_output
