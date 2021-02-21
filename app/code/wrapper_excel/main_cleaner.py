# -*- coding: utf-8 -*-

class MainCleanerExcel():
    def __init__(self, ExcelToDataframe, CleanerDataframe, IntelligentFill, ReviewerDataframe):
        self.ExcelToDataframe = ExcelToDataframe
        self.CleanerDf = CleanerDataframe
        self.IntellFill = IntelligentFill
        self.ReviewerDataframe = ReviewerDataframe
        
    def updateExcel(self):
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
        dataframe.to_excel(self.ExcelToDataframe.AccessExcel.ExcelPath.copiedExcelPath())



    def getDataframeAndEqCol(self):
        return self.ExcelToDataframe.getDataframeAndEqCol()

