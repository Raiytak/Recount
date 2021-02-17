# -*- coding: utf-8 -*-
import unidecode

import numpy as np
import pandas as pd


class CleanerDataframe():
    def addDateEverywhere(self, dataframe):
        last_date = np.datetime64("2019-07-01")
        for i in range(len(dataframe)):
            current_date = dataframe.loc[i,"Quand"]
            if pd.isnull(current_date):
                dataframe.at[i,"Quand"] = last_date
            else:
                last_date = current_date
        return dataframe
                
    def convertDateToStr(self, dataframe):
        def convertDatetimeToSQLFormat(datetime_elem):
            time_sql_format = datetime_elem.strftime("%Y-%m-%d")
            return time_sql_format
        dataframe["Date"] = dataframe["Quand"].apply(convertDatetimeToSQLFormat)
        return dataframe
    
    def removeSummationLines(self, dataframe):
        for i in range(len(dataframe)):
            current_line = dataframe.loc[i]
            if pd.isnull(current_line["Dépenses Euros"]) and pd.isnull(current_line["Dépenses Dollars"]):
                dataframe = dataframe.drop(i)
        return dataframe
    
    def addSummarizedExpensesColumn(self, dataframe):
        list_expenses = self.getListExpenses(dataframe)
        dataframe.insert(loc=0, column="Dépenses", value=list_expenses)
        return dataframe

    def getListExpenses(self, dataframe):
        df_expenses = dataframe.loc[:,["Dépenses Euros", "Dépenses Dollars"]]
        df_expenses = df_expenses.fillna(0) #Fill the nan values with 0
        df_expenses = [self.convertExpenseInEuros(row) for index, row in df_expenses.iterrows()]
        return df_expenses
    
    def convertExpenseInEuros(self, row):
        expenseE = row["Dépenses Euros"]
        expenseD = row["Dépenses Dollars"]
        return np.around(expenseE + (expenseD/1.5), 2) #Limit the number of digits to 2
    
    def removeRawExpensesColumns(self, dataframe):
        dataframe = dataframe.drop(columns=["Dépenses Euros", "Dépenses Dollars"])
        return dataframe
    
    def removeUselessColumns(self, dataframe):
        list_columns = ["Thème", "Quoi", "Quand",
                        "Somme euro", "Somme dollar", "Sommes E", "Sommes D",
                        "Excédentaires E", "Excédentaires D"]
        dataframe = dataframe.drop(columns=list_columns)
        return dataframe
        
    
    def normalizeDescription(self, dataframe):
        dataframe["Quoi"] = dataframe["Quoi"].apply(self.removeAccentAndLowerStr)
        return dataframe
        
        
    def splitAndCleanTheme(self, dataframe):
        def convertIntoTheme(theme_subtheme):
            theme_subtheme = str(theme_subtheme)
            list_tst = theme_subtheme.split(":")
            if list_tst != []:
                return list_tst[0]
        def convertIntoSubtheme(theme_subtheme):
            theme_subtheme = str(theme_subtheme)
            list_tst = theme_subtheme.split(":")
            if len(list_tst) > 1:
                return list_tst[1]
            return str(np.nan)       
        dataframe["Theme"] = dataframe["Thème"].apply(convertIntoTheme)
        dataframe["Soustheme"] = dataframe["Thème"].apply(convertIntoSubtheme)
        return dataframe
        
        
    def splitAndCleanDescription(self, dataframe):
        def isOnlyEnterprise(raw_description):
            splited_descr = raw_description.split()
            if len(splited_descr) > 1:
                return False
            resplited_descr = splited_descr[0].split(":")
            resplited_descr = self.removeSpaceInList(resplited_descr)
            if len(resplited_descr) > 1:
                return False
            return True
        def convertIntoEnterprise(raw_description):
            if isOnlyEnterprise(raw_description):
                return raw_description
            list_descr = raw_description.split(":")
            list_descr = self.removeSpaceInList(list_descr)
            if len(list_descr) > 1:
                entreprise = list_descr[0]
                if entreprise == "":
                    return str(np.nan)
                return list_descr[0]
            return str(np.nan)
        def convertIntoDescription(raw_description):
            if isOnlyEnterprise(raw_description):
                return str(np.nan)
            list_descr = raw_description.split(":")
            if len(list_descr) > 1:
                return list_descr[1]
            return list_descr[0]
        dataframe["Entreprise"] = dataframe["Quoi"].apply(convertIntoEnterprise)
        dataframe["Description"] = dataframe["Quoi"].apply(convertIntoDescription)
        return dataframe
        
    def removeAllApostrophes(self, dataframe):
        list_to_normalize = ["Entreprise", "Description"]
        for column in list_to_normalize:
            dataframe[column] = dataframe[column].apply(self.removeApostrophe)
        return dataframe
        
    def removeAccentAndLowerStr(self, text):
        text = unidecode.unidecode(text) #Remove accents
        text = text.lower()
        return text
    
    def removeApostrophe(self, text):
        #Have to remove the apostrophes for the pymysql that doesn't support it
        text = text.replace("'"," ")
        return text
        
    def removeSpaceInList(self, list_text):
        list_ret = []
        for text in list_text:
            if text!= "":
                first_text = text
                if text[0] == " ":
                    first_text=first_text[1:]
                second_text = first_text
                if text[-1] == " ":
                    second_text=second_text[:-1]
                list_ret.append(second_text)
        return list_ret
    

