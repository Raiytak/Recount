import os
import io
import base64

import update_db



class FileSaver():
    def __init__(self, AccessExcel):
        self.AccessExcel = AccessExcel
        self.path_to_save = self.AccessExcel.ExcelPath.getDataPath()
        self.name_imported_excel = self.AccessExcel.ExcelPath.nameImportedExcel()
        # self.removeOlderImportedFile()
        

    def removeOlderImportedFile(self):
        for file_format in ["xlsx","csv"]:
            try:
                path_file = self.path_to_save + "/" + self.name_imported_excel + "." + file_format
                os.remove(path_file)
            except FileNotFoundError:
                pass

    def decodeImportedFile(self, content_type, content):
        if "xml" in content_type:
            decodedFile = io.BytesIO(content)
            file_format = "xlsx"
        elif "csv" in content_type:
            decodedFile = content.decode('utf-8')
            file_format = "csv"
        return decodedFile, file_format

    def saveFile(self, file_in_str):
        # Nothing to register
        if file_in_str == None:
            return 0

        self.removeOlderImportedFile()

        content_type, content_string = file_in_str.split(',')
        file_in_str = base64.b64decode(content_string)

        decodedFile, file_format = self.decodeImportedFile(content_type, file_in_str)
        path_file = self.path_to_save + "/" + self.name_imported_excel + "." + file_format

        if "xml" in content_type:
            with open(path_file, 'wb') as f:
                f.write(decodedFile.read())
        elif "csv" in content_type:
            with open(path_file, 'w') as f:
                f.write(decodedFile)

        self.AccessExcel.copyImportedExcel()
        update_db.updateAll()