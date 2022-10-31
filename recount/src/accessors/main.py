from file_management import *
from accessors.file_management import UserManager
from excel_manager import ExcelManager

DEFAULT_FOLDERS = [
    RootFolder,
    DataFolder,
    LogFolder,
    AssetFolder,
    ConfigFolder,
    LoginFolder,
    KeyFolder,
    UsersFolder,
]


def removeFolders():
    RootFolder.removeFolder()


def initializeFolders():
    for folder_manager in DEFAULT_FOLDERS:
        folder_manager.createFolder()


def generateDefaultExcelKey():
    key = KeyManager()
    if not key._DEFAULT_EXCEL_KEY.exists():
        key.generateKey(key._DEFAULT_EXCEL_KEY_NAME)


def copyAssetFiles():
    AssetFolder.copyDefaultAssets()


def copyExampleAppConfig():
    ConfigFolder.copyExampleConfig()


def copyExampleLogin():
    LoginManager.copyExample()


def createUserFolder(user_manager):
    user_manager.createFolder()


def removeUserFolder(user_manager):
    user_manager.removeFolder()


def copyExampleExcel(user_manager):
    user_manager.copyExampleExcel()


def removeDefaultExcel(user_manager):
    user_manager.removeDefaultExcel()


def encryptFileOfUser(excel_manager: ExcelManager, filename: str):
    df = excel_manager.dataframe(filename=filename)
    excel_manager.saveDataframe(df, filename)


def decryptFileOfUser(excel_manager: ExcelManager, filename: str):
    df = excel_manager.dataframe(filename=filename)
    excel_manager.saveDataframe(df, filename, encrypt=False)


# from currency_converter import ECB_URL


#     def updateCurrenciesRates():
#         # Delete the older file
#         for filename in ConfigPath.currencies_rates_filenames:
#             ConfigManager.removeFile(ConfigPath.ROOT / filename)
#         # Import the CURRENCIES rates up to date
#         urllib.request.urlretrieve(ECB_URL, ConfigPath.currencies_rates)
# IDEA: get a database for the currencies conversion, request only necessaries (graphql?)
