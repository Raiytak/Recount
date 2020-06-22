import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import unidecode


def getDate(my_date):
    try:
        formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S.%f")
        return formated_date
    except ValueError:
        pass
    
    try:
        formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%d")
        return formated_date
    except ValueError:
        pass
    
    raise Exception
    
    
def update_dict_with_lists(dictA, dictB):
    for key, value in dictB.items():
        if key not in dictA.keys():
            dictA[key] = value
        else:
            for subkey, subvalue in value.items():
                if type(subvalue) == list:
                    dictA[key][subkey] += subvalue
    return dictA


def convertStrIntoThemeSubThemes(str_to_convert):
    if str_to_convert == None:
        return "NOT DECLARED"
    dict_tSt = {}
    list_themes = str_to_convert.split(";")
    for tSt_theme in list_themes:
        list_tStheme = tSt_theme.split(":")
        theme = list_tStheme.pop(0)
        subThemes = []
        if list_tStheme != []:
            subThemes = list_tStheme[0].split("+")
        dict_tSt[theme] = subThemes
    return theme


def convertStrIntoSubThemes(str_to_convert):
    if str_to_convert == None:
        return None
    # dict_tSt = {}
    list_themes = str_to_convert.split(";")
    for tSt_theme in list_themes:
        list_tStheme = tSt_theme.split(":")
        theme = list_tStheme.pop(0)
        subThemes = []
        if list_tStheme == []:
            return "NOT DECLARED"
        
        subThemes = list_tStheme[0].split("+")
        if subThemes[0] == "":
            return "commun"
        else:
            return subThemes[0]
    #     dict_tSt[theme] = subThemes
    # return theme
    
    
def removeAccentAndApostropheInStr(element_to_clean):
    if type(element_to_clean) != str:
        return element_to_clean
    else:
        text = element_to_clean
        
        #Remove accents
        text = unidecode.unidecode(text)
        #Have to remove the apostrophes for the pymysql that doesn't support it
        text = text.replace("'", " ")

        return text