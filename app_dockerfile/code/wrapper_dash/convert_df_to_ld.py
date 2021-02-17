import numpy as np




class DataframeToListOfDicts(): #logic
    def convertDataframeToListOfDicts(self, dataframe, type_graph):
        if type_graph == "all-scatter":
            # dataframe = dataframe[dataframe["theme"].isnull() == False]
            list_dict_expenses = self.convertDataframeToExpensesByColumn(dataframe, "theme")
            return list_dict_expenses
        
        if type_graph == "theme-pie":
            # dataframe = dataframe[dataframe["theme"]=="alimentaire"]
            list_dict_expenses = self.convertDataframeToSumExpensesByColumn(dataframe, "theme")
            return list_dict_expenses
        
        if type_graph == "mean-bar":
            list_dataframes = dataframe
            # for df in list_dataframes:
            #     df = df[df["theme"].isnull() == False]
            list_dict_expenses = self.convertListDataframeByWeekToExpensesByColumn(dataframe, "theme")
            return list_dict_expenses
        
        if type_graph == "food-bar":
            list_dataframes = []
            for df in dataframe:
                df = df[df["theme"]=="alimentaire"]
                new_df = df[df["soustheme"].isnull() == False]
                list_dataframes.append(new_df)
                
            list_dict_expenses = self.convertListDataframeByWeekToExpensesByColumn(list_dataframes, "soustheme")
            return list_dict_expenses
        
        raise ValueError
        
        
        
    def convertDataframeToExpensesByColumn(self, dataframe, column_name):
        data = dataframe
        unique_theme = [val for val in data[column_name].unique() if val is not None]
        list_dict_expenses = [dict(
                x=data[data[column_name] == i]["date"],
                y=data[data[column_name] == i]["montant"],
                text=data[data[column_name] == i]["description"],
                name = i
            ) for i in unique_theme]
        list_dict_expenses.sort(key=sortByName)
        return list_dict_expenses
        
    def convertDataframeToSumExpensesByColumn(self, dataframe, column_name):
        data = dataframe
        list_dict_expenses = {"values":[], "names":[], "labels":[]}
        unique_theme = [val for val in data[column_name].unique() if val is not None]
        unique_theme.sort()
        for i in unique_theme:
            list_dict_expenses["values"].append(np.sum(data[data[column_name]==i]["montant"]))
            list_dict_expenses["names"].append(i)
            list_dict_expenses["labels"].append(i)
        return [list_dict_expenses]    
    
    
    
    def convertListDataframeByWeekToExpensesByColumn(self, list_dataframe_by_week, column_name):
        dict_returned = {}
        for dataframe in list_dataframe_by_week:
            data = dataframe
            unique_theme = [val for val in data[column_name].unique() if val is not None]
            dict_expenses = {i:dict(
                    x=[data.iloc[0]["date_week"]],
                    y=[np.sum(data[data[column_name] == i]["montant"])],
                    name = i
                ) for i in unique_theme}
            updateDictWithLists(dict_returned, dict_expenses)
        list_dict_expenses = list(dict_returned.values())
        list_dict_expenses.sort(key=sortByName, reverse=True)
        return list_dict_expenses
    
    
    
    
    def convertDataframeOfWeeksToListOfDicts(self, dataframe_by_week, type_graph): #dataframe of format [ [datetime.datetime(xxx), dataframe], ... ]
        if type_graph == "mean-bar":
            list_dict_expenses = self.convertDataframeToMeanByWeek(dataframe_by_week)
            return list_dict_expenses
        
        if type_graph == "food-bar":
            list_dict_expenses = self.convertDataframeToFoodByWeek(dataframe_by_week)
            return list_dict_expenses
        
    def convertDataframeToFoodByWeek(self, dataframe_by_week):
        dict_prep_expenses = {}
        for date, data in dataframe_by_week:
            if data.empty:
                dict_expenses_week = {}
            else:
                data_alim = data["theme" == "alimentaire"]
                unique_theme = data_alim["subtheme"].unique()
                dict_expenses_week = {i:dict(
                        x=[date],
                        y=[np.sum(data[data["subtheme"] == i]["montant"])],
                        name = i
                    ) for i in unique_theme}
            dict_prep_expenses = updateDictWithLists(dict_prep_expenses, dict_expenses_week)
            
        list_dict_expenses = list(dict_prep_expenses.values())
        list_dict_expenses.sort(key=sortByName)
        return list_dict_expenses
        
    def convertDataframeToMeanByWeek(self, dataframe_by_week):
        dict_prep_expenses = {}
        for date, data in dataframe_by_week:
            if data.empty:
                dict_expenses_week = {}
            else:
                unique_theme = data["theme"].unique()
                dict_expenses_week = {i:dict(
                        x=[date],
                        y=[np.sum(data[data["theme"] == i]["montant"])],
                        name = i
                    ) for i in unique_theme}
            dict_prep_expenses = updateDictWithLists(dict_prep_expenses, dict_expenses_week)
            
        list_dict_expenses = list(dict_prep_expenses.values())
        list_dict_expenses.sort(key=sortByName)
        return list_dict_expenses
        

    
    
def updateDictWithLists(dictA, dictB):
    for key, value in dictB.items():
        if key not in dictA.keys():
            dictA[key] = value
        else:
            for subkey, subvalue in value.items():
                if type(subvalue) == list:
                    dictA[key][subkey] += subvalue
    return dictA


def sortByName(dict_named):
    return dict_named["name"]