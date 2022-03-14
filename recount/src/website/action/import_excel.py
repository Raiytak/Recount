# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Save the excel imported by the user.
"""

# TODO: check the conformity of the imported excel
# TODO: if not conform, notify the user
#   give the choice to give another one or to use the defaul excel

import io
import base64

# import pandas as pd

import logs
from access.access_files import UserFilesAccess


def saveImportedFile(username, file_imported):
    # If there is nothing to save, the function stops
    if file_imported != None:
        user_file = UserFilesAccess(username)

        # print(file_imported[100]) TODO: ?
        logs.formatAndDisplay(f"{username}: Importing file ...")
        content_type, buffer_content = decodeImportedFile(file_imported)
        file_data = buffer_content.read()
        checkIsXlsxFile(content_type)
        user_file.saveExcel(file_data)
        logs.formatAndDisplay(f"{username}: File imported")


def decodeImportedFile(file_imported):
    content_type_encoded, content_string_encoded = file_imported.split(",")
    content_type, content_decoded = getTypeAndDecodeImportedFile(
        content_type_encoded, content_string_encoded
    )
    return content_type, content_decoded


def getTypeAndDecodeImportedFile(content_type_encoded, content_string_encoded):
    content_string_base64 = base64.b64decode(content_string_encoded)
    if ("xml" in content_type_encoded) or ("xls" in content_type_encoded):
        content_decoded = io.BytesIO(content_string_base64)
        content_type = "xlsx"
    else:
        content_type = content_type_encoded
    return content_type, content_decoded


# TODO: stronger check
def checkIsXlsxFile(content_type):
    if content_type != "xlsx":
        raise TypeError("The file imported is not a '.xlsx' file")

    # def saveNotebookDataTorawExcel(data_excel):
    #     # If there is nothing to save, the function stops
    #     try:
    #         dataframe = pd.DataFrame(data_excel)
    #         dataframe.to_excel(ExcelPaths.rawCopiedExcelPath(), index=False)
    #     except Exception:
    #         # print(" >>> An error has occcured during the update.<<<\n >>> Please check the values you have inserted <<<")
    #         return " >>> An error has occcured during the update. Please check the values you have inserted <<<"

    #     return "Update done"

    # def translateDataframeToNotebookData(dataframe):
    #     data_for_output = dataframe.to_dict("records")
    #     return data_for_output
