import datetime
from dateutil.relativedelta import relativedelta

import wrapper_sql.wrapper_sql as wrapper_sql

import config.access_config as access_config
myAccessConfig = access_config.AccessConfig()
config_json = myAccessConfig.getConfig()


class DateToDataframe:
    def __init__(self):
        self.bd_sql = wrapper_sql.WrapperOfTable("depenses_propres", config_json)
        self.translator = wrapper_sql.ResponseSqlToDataframe()
    
    def getListDataframeByWeekFromDate(self, start_date, periode):
        current_date = self._convertToDatetime(start_date)
        list_dataframe = []
        end_date = self._convertPeriodeToDate(current_date, periode)
        while current_date < end_date:
            dataframe = self.getDataframeFromDate(current_date, "week")
            dataframe["date_week"] = self.getYMDatetime(current_date)
            if dataframe.empty == False:
                list_dataframe.append(dataframe)
            current_date = self._addWeek(current_date)
        return list_dataframe
    
    def getDataframeFromDate(self, start_date, periode):
        start_date = self._convertToDatetime(start_date)
        end_date = self._convertPeriodeToDate(start_date, periode)
        dataframe = self._convertDateToDataframe(start_date, end_date)
        return dataframe
        
    
    def _convertDateToDataframe(self, start_date, end_date):
        start_date = self._convertToDatetime(start_date)
        request = self.convertDateToRequestSQL(start_date, end_date)
        reponse = self.bd_sql.select(request)
        # print("Reponse : " + reponse)
        dataframe = self._translateSqlToDataframe(reponse)
        return dataframe
        
        
    def convertDateToRequestSQL(self, start_date, end_date):
        start_date = self._convertToDatetime(start_date)
        start_req = "SELECT * FROM & WHERE date >= "
        mid_req = self._getDatetimeInGoodShape(start_date)+" AND date < "
        end_req = self._getDatetimeInGoodShape(end_date)
        request = start_req + mid_req + end_req
        return request
    
    def _getDatetimeInGoodShape(self, my_datetime):
        datetime_good_shape = self.getYMDatetime(my_datetime)
        return "'"+datetime_good_shape+"'"

    def _translateSqlToDataframe(self, response):
        dataframe = self.translator.translateResponseSqlToDataframe(response, self.bd_sql)
        return dataframe
    
    
    def _convertPeriodeToDate(self, start_date, periode):
        start_date = self._convertToDatetime(start_date)
        end_date = start_date        
        if periode == "week":
            end_date += relativedelta(weeks=1)
        elif periode == "month":
            end_date += relativedelta(months=1)
            end_date -= relativedelta(days=1)
        elif periode == "semestre":
            end_date += relativedelta(months=4)
            end_date -= relativedelta(days=1)
        else:
            print("Period not accepted : \nonly 'week', 'month' and 'semestre' are authoriezd")
            raise Exception
        return end_date
    
    def _addWeek(self, current_date):
        current_date = current_date + relativedelta(weeks=1)
        return current_date
    
    def getYMDatetime(self, my_datetime):
        return my_datetime.strftime("%Y-%m-%d")

    def _convertToDatetime(self, my_date):
        if type(my_date) == datetime.datetime:
            return my_date
        try:
            formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S.%f")
            return formated_date
        except ValueError:
            pass
        try:
            formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S")
            return formated_date
        except ValueError:
            pass
        try:
            formated_date = datetime.datetime.strptime(my_date, "%Y-%m-%d")
            return formated_date
        except ValueError:
            pass
        raise Exception
    