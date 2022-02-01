# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Clean the raw_excel into clean_excel using the classes of this folder and the pandas'
dataframe functionalities.
"""

from wrapper_excel.check_conformity import ReviewerDataframe
from wrapper_excel.cleaner_dataframe import CleanerDataframe
from wrapper_excel.excel_to_df import ExcelToDataframe
from wrapper_excel.fill_blanks import IntelligentFill
from accessors.data_encryption import ExcelEncryption


class MainCleanerExcel:
    """Clean raw_excel into clean excel using pandas' dataframe"""

    def __init__(self, username=""):
        self.username = username
        self.ExcelToDataframe = ExcelToDataframe(self.username)
        self.CleanerDf = CleanerDataframe()
        self.IntellFill = IntelligentFill()
        self.ReviewerDataframe = ReviewerDataframe()
        self.ExcelEncryption = ExcelEncryption()

    def updateExcel(self):
        self.ExcelToDataframe.AccessUserFiles.AccessExcel.updateUserExcel()
        dataframe = self.ExcelToDataframe.getDataframe()

        dataframe = self.CleanerDf.addDateEverywhere(dataframe)
        dataframe = self.CleanerDf.convertDateToStr(dataframe)

        dataframe = self.CleanerDf.removeSummationLines(dataframe)
        dataframe = self.CleanerDf.addSummarizedExpensesColumn(dataframe)
        dataframe = self.CleanerDf.removeRawExpensesColumns(dataframe)

        dataframe = self.CleanerDf.normalizeDescription(dataframe)
        dataframe = self.CleanerDf.splitAndCleanCategory(dataframe)
        dataframe = self.CleanerDf.splitAndCleanDescription(dataframe)

        dataframe = self.IntellFill.intelligentFillBlankCategoryUsingCompany(dataframe)

        dataframe = self.CleanerDf.removeUselessColumns(dataframe)
        dataframe = self.CleanerDf.removeAllApostrophes(dataframe)

        # This function shows on the CLI if there are inputs of the excel that are not allowed (mostly for syntax errors)
        self.ReviewerDataframe.checkConformity(dataframe)

        # Save the dataframe create into the appropriate excel (this must be copy_expenses.xlsx)
        self.saveDataframeToCopiedExcel(dataframe)

    def getDataframeAndEqCol(self):
        return self.ExcelToDataframe.getDataframeAndEqCol()

    def saveDataframeToCopiedExcel(self, dataframe):
        path_excel = self.ExcelToDataframe.AccessExcel.ExcelPaths.cleanedExcelPath()
        self.ExcelEncryption.encryptDataframe(dataframe, path_excel)
        # dataframe.to_excel(
        #     self.ExcelToDataframe.AccessExcel.ExcelPaths.cleanedExcelPath()
        # )
