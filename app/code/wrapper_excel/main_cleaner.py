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
        dataframe = self.CleanerDf.splitAndCleanTheme(dataframe)
        dataframe = self.CleanerDf.splitAndCleanDescription(dataframe)
        
        dataframe = self.IntellFill.intelligentFillBlankThemeUsingEntreprise(dataframe)
        
        dataframe = self.CleanerDf.removeUselessColumns(dataframe)
        dataframe = self.CleanerDf.removeAllApostrophes(dataframe)
        
        
        self.ReviewerDataframe.checkConformity(dataframe)
        
        dataframe.to_excel(self.ExcelToDataframe.AccessExcel.ExcelPaths.excel_path)



    def getDataframeAndEqCol(self):
        return self.ExcelToDataframe.getDataframeAndEqCol()

