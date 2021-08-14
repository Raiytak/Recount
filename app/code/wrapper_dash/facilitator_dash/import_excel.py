import io
import base64
import pandas as pd

from accessors.access_files import AccessUserFiles
from accessors.data_encryption import ExcelEncryption
from wrapper_excel.excel_to_df import ExcelToDataframe

import update_data

import logging
from logs.logs import paddedLogMessage


class ImportExcelFileSaver:
    def __init__(self):
        self.ExcelToDataframe = ExcelToDataframe()
        self.ExcelEncryption = ExcelEncryption()
        self.ExcelPaths = self.ExcelToDataframe.ExcelPaths

    def saveImportedFile(self, username, file_imported):
        # If there is nothing to save, the function stops
        if file_imported != None:
            logging.info(paddedLogMessage(f"{username}: Importing file ..."))
            try:
                content_type, buffer_content = self.decodeImportedFile(file_imported)
                file_data = buffer_content.read()
                self.checkIsXlsxFile(content_type)
                self.saveContentStringIntoXlsxFile(username, file_data)

                update_data.updateAll(username)
                logging.info(
                    paddedLogMessage(f"{username}: File imported, update done")
                )

            except TypeError:
                logging.error(
                    paddedLogMessage(
                        f"{username}: The file imported is not a '.xlsx' file"
                    )
                )

    def decodeImportedFile(self, file_imported):
        (
            content_type_encoded,
            content_string_encoded,
        ) = self.getContentTypeAndStringOfImportedFile(file_imported)
        content_type, content_decoded = self.getTypeAndDecodeImportedFile(
            content_type_encoded, content_string_encoded
        )
        return content_type, content_decoded

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

    def saveContentStringIntoXlsxFile(self, username, file_data):
        myAccessUserFiles = AccessUserFiles(username)
        path_file = myAccessUserFiles.AccessExcel.ExcelPaths.importedExcelPath()
        self.ExcelEncryption.encryptAndSaveDataToPath(file_data, path_file)
        myAccessUserFiles.AccessExcel.updateUserExcel()

    def checkIsXlsxFile(self, content_type):
        if content_type != "xlsx":
            raise TypeError("The file imported is not a '.xlsx' file")

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
