# -*- coding: utf-8 -*-

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

# from currency_converter import ECB_URL


def initializeFolders():
    return

    def __init__(self, username: str = None):
        self.fernet_encryption = FileEncryption(ConfigManager.EXCEL_KEY)
        if username is None:
            self.user_files_path = UserFilesPath
        else:
            self.user_files_path = UserFilesPath(username)
            self.initializeUserFolder()
            if self.isEmpty:
                self.useExamples()

    def initializeUserFolder(self):
        if not self.user_files_path.user_folder.exists():
            self.createUserFolder()

    def useExamples(self):
        if not self.user_files_path.excel.exists():
            self.copyAndEncryptExampleExcel()
        if not self.user_files_path.categories.exists():
            shutil.copy(
                UserFilesPath.example_categories, self.user_files_path.categories
            )
        if not self.user_files_path.translations.exists():
            shutil.copy(
                UserFilesPath.example_translations, self.user_files_path.translations,
            )

    def __init__():

        self.initializeUserFolder()
        if self.isEmpty:
            self.useExamples()

    # TODO: generate fernet key

    def copyAndEncryptExampleExcel(self):
        data = self.excel(UserFilesPath.example_excel)
        self.saveExcel(data)

    def isExchangeRatesFileUpToDate():
        if len(ConfigPath.currencies_rates_filenames) == 0:
            return False
        return (
            ConfigPath.currencies_rates.name
            == ConfigPath.today_currencies_rates_filename
        )

    def updateCurrenciesRates():
        # Delete the older file
        for filename in ConfigPath.currencies_rates_filenames:
            ConfigManager.removeFile(ConfigPath.ROOT / filename)
        # Import the CURRENCIES rates up to date
        urllib.request.urlretrieve(ECB_URL, ConfigPath.currencies_rates)

