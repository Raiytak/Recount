import os
import io
import base64
import csv
import pandas as pd

import update_db


class FileSaver():
    def __init__(self, ExcelToDataframe):
        self.ExcelToDataframe = ExcelToDataframe
        self.AccessExcel = self.ExcelToDataframe.AccessExcel
        self.ExcelPath = self.AccessExcel.ExcelPath
        

    def removeOlderImportedFile(self):
        try:
            path_file = self.ExcelPath.importedExcelPath()
            os.remove(path_file)
        except FileNotFoundError:
            pass
    def removeTemporaryImportedFileOfTypeCSV(self):
        try:
            path_file = self.name_imported_excel_type_csv_temporary()
            os.remove(path_file)
        except FileNotFoundError:
            pass




    def getContentTypeAndStringOfImportedFile(self, file_imported):
        content_type, content_string_encoded = file_imported.split(',')
        return content_type, content_string_encoded

    def selectTypeAndDecodeImportedFile(self, content_type_encoded, content_string_encoded):
        content_string_base64 = base64.b64decode(content_string_encoded)
        if ("xml" in content_type_encoded) or ("xls" in content_type_encoded) :
            content_decoded = io.BytesIO(content_string_base64)
            content_type = "xlsx"
        elif "csv" in content_type_encoded:
            content_decoded = content_string_base64.decode('utf-8')
            content_type = "csv"
        return content_type, content_decoded


    def decodeImportedFile(self, file_imported):
        content_type_encoded, content_string_encoded = self.getContentTypeAndStringOfImportedFile(file_imported)
        content_type, content_decoded = self.selectTypeAndDecodeImportedFile(content_type_encoded, content_string_encoded)
        return content_type, content_decoded
        


    def saveContentStringIntoXlsxFile(self, content_type, content_decoded):
        path_file = self.ExcelPath.importedExcelPath()
        if content_type == "xlsx" :
            with open(path_file, 'wb') as f:
                f.write(content_decoded.read())
        # If the file imported is in csv, there is an additional step to convert this file into xlsx
        elif content_type == "csv":
            path_temporary_csv = self.ExcelPath.importedTemporaryCSVExcelPath()

            keys = list(content_decoded[0].keys())
            with open(path_temporary_csv, 'w', encoding='utf8', newline='') as output_file:
                writer = csv.DictWriter(output_file, fieldnames=keys, delimiter=";")
                writer.writeheader()
                writer.writerows(content_decoded)

            dataframe = pd.read_csv(path_temporary_csv)
            dataframe.to_excel(path_file)
            self.removeTemporaryImportedFileOfTypeCSV()


    def saveImportedFile(self, file_imported):
        # If there is nothing to save, the function stops
        if file_imported != None:
            content_type, content_decoded = self.decodeImportedFile(file_imported)
            self.saveContentStringIntoXlsxFile(content_type, content_decoded)
            self.AccessExcel.updateExcel()
            # update_db.updateAll()


    def saveTemporaryRawExcelFromInputData(self, data_excel):
        # If there is nothing to save, the function stops
        dataframe = pd.DataFrame(data_excel)
        dataframe.to_excel(self.ExcelPath.rawCopiedExcelPath(), index=False)



    def getDataframeOfImportedFileIfExists(self):
        if self.ExcelPath.importedExcelExists() == True:
            return self.AccessExcel.getDataframeOfImportedFile()
        else:
            return 0



    def translateDataframeToData(self, dataframe):
        data_for_output = dataframe.to_dict('records')
        return data_for_output