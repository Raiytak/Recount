from file_management import *

DEFAULT_FOLDERS = [
    RootFolder,
    DataFolder,
    LogFolder,
    AssetFolder,
    ConfigFolder,
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


def copyAppExampleConfig():
    ConfigFolder.copyExampleConfig()


def createUserFolder(user_manager):
    user_manager.createFolder()


def removeUserFolder(user_manager):
    user_manager.removeFolder()


def copyExampleExcel(user_manager):
    user_manager.copyExampleExcel()


def removeDefaultExcel(user_manager):
    user_manager.removeDefaultExcel()
