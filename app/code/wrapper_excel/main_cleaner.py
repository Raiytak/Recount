# -*- coding: utf-8 -*-
from wrapper_excel.check_conformity import ReviewerDataframe
from wrapper_excel.cleaner_dataframe import CleanerDataframe
from wrapper_excel.convert_excel_to_df import ExcelToDataframe
from wrapper_excel.fill_blanks import IntelligentFill


class MainCleanerExcel:
    def __init__(self, username=""):
        self.username = username
        self.ExcelToDataframe = ExcelToDataframe(self.username)
        self.CleanerDf = CleanerDataframe()
        self.IntellFill = IntelligentFill()
        self.ReviewerDataframe = ReviewerDataframe()

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
        # self.ExcelToDataframe.AccessExcel.removeCopiedExcel()
        dataframe.to_excel(
            self.ExcelToDataframe.AccessExcel.ExcelPaths.cleanedExcelPath()
        )
