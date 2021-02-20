import random


class ListDictToGraph(): #add metadata
    def __init__(self, autorized_tst_json):
        self.ColorSetter = ColorSetter(autorized_tst_json)
        self.getColor = self.ColorSetter.convertThemeToColor
        self.getListColors = self.ColorSetter.convertListThemeToListColor
    
    
    def getGraph(self, list_dict_of_expenses, type_graph): #main of class
        if type_graph == "all-scatter":
            graph = self.scatterGraph(list_dict_of_expenses)
            return graph
        
        if type_graph == "theme-pie":
            graph = self.pieGraph(list_dict_of_expenses)
            return graph
        
        if type_graph == "mean-bar":
            graph = self.meanGraph(list_dict_of_expenses)
            return graph
        
        if type_graph == "food-bar":
            graph = self.foodGraph(list_dict_of_expenses)
            return graph
        
        raise ValueError
    
    
    
    def scatterGraph(self, list_dict_of_expenses): #Needs list expenses by theme
        list_data = []
        for dict_exp in list_dict_of_expenses:
            dict_exp["mode"] = "markers"
            dict_exp["marker"] = {"color":self.getColor(dict_exp["name"])}
            dict_exp["hoverinfo"] = "text+y+x"
            list_data.append(dict_exp)
        fig_data = {"data":list_data,
                    "layout":{"title":{"text":"Dépenses par thème"},
                              "yaxis": {"type": "log", "title":"Dépenses (euros)"},
                              "xaxis":{"title":"Jour"}}
        }
        return fig_data
    
    def pieGraph(self, list_dict_of_expenses): #Needs one list with the sum of the expenses by theme
        list_dict_of_expenses[0]["type"] = "pie"
        list_dict_of_expenses[0]["marker"] = {"colors":self.getListColors(list_dict_of_expenses[0]["names"])}
        fig_data = {"data":list_dict_of_expenses,
                    "layout":{"title":{"text":"Camembert des thèmes"}}
        }
        return fig_data
    
    
    def meanGraph(self, list_dict_of_expenses): #Needs list by week of the expenses by theme
        list_data = []
        for dict_exp in list_dict_of_expenses:
            dict_exp["type"] = "bar"
            dict_exp["marker"] = {"color":self.getColor(dict_exp["name"])}
            list_data.append(dict_exp)
        fig_data = {"data":list_data,
                    "layout":{"title":{"text":"Total des dépenses par semaine"},
                              "barmode":"stack",
                              "yaxis": {"title":"Dépenses (euros)"},
                              "xaxis":{"title":"Jour"}}
        }
        return fig_data
    
    def foodGraph(self, list_dict_of_expenses): #Needs list by week of the expenses of alimentaire by theme
        list_data = []
        for dict_exp in list_dict_of_expenses:
            dict_exp["type"] = "bar"
            dict_exp["marker"] = {"color":self.getColor(dict_exp["name"])}
            list_data.append(dict_exp)
        fig_data = {"data":list_data,
                    "layout":{"title":{"text":"Dépenses par semaine en nourriture"},
                              "barmode":"stack",
                              "yaxis": {"title":"Dépenses (euros)"},
                              "xaxis":{"title":"Jour"}}
        }
        return fig_data
    


class ColorSetter():
    def __init__(self, autorized_tst_json):
        self.autorized_tst_json = autorized_tst_json
        self.colors_json = self._getColorsJson()
    
    def convertThemeToColor(self, theme):
        if theme in self.colors_json.keys():
            return self.colors_json[theme]
        return ""
    
    def convertListThemeToListColor(self, list_theme):
        list_colors = []
        for theme in list_theme:
            if theme in self.colors_json.keys():
                list_colors.append(self.colors_json[theme])
            else:
                list_colors.append("")
                print("not in list")
        return list_colors
    
    
    def _getAllAvailableThemes(self):
        list_themes = list(self.autorized_tst_json.keys())
        return list_themes
    
    def _getColorsJson(self):
        colors_json = {}
        list_themes = self._getAllAvailableThemes()
        random.shuffle(list_themes)
        list_available_colors = self._getColors(list_themes)
        for theme, color in zip(list_themes, list_available_colors):
            colors_json[theme] = color
        return colors_json
    
    def _getColors(self, list_themes):
        list_available_colors = ["navy", "royalblue", "lime", "crimson", "slategray", "darkred", "khaki", "darkgreen", "chocolate"]
        len_colors = len(list_available_colors)
        len_themes = len(list_themes)
        if len_colors > len_themes:
            return list_available_colors
        other_colors = ["orange", "b", "c", "g", "m", "y", "r", "k"]
        list_available_colors += other_colors
        len_themes = len(list_themes)
        if len_colors < len_themes:
            print("Not enough color")
            raise Exception
        return list_available_colors