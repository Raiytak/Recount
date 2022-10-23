from accessors.file_management import UserManager
from excel_manager import ExcelManager


def encryptFileOfUser(excel_manager: ExcelManager, filename: str):
    df = excel_manager.dataframe(filename=filename)
    excel_manager.saveDataframe(df, filename)


def decryptFileOfUser(excel_manager: ExcelManager, filename: str):
    df = excel_manager.dataframe(filename=filename)
    excel_manager.saveDataframe(df, filename, encrypt=False)
