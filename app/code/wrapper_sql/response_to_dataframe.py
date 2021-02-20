import pandas as pd
import numpy as np



class ResponseSqlToDataframe():
    def translateResponseSqlToDataframe(self, response_sql, wrapper_table):
        dataframe = pd.DataFrame(response_sql)
        columns_name = wrapper_table.getNameColumns()

        # If data exists in the period selected, the the dataframe is not empty and can be returned right away
        if dataframe.empty == False:
            dataframe.columns = columns_name
            return dataframe
        # Else we have to create a dataframe with empty values
        else:
            dataframe = self.getDataframeWithEmptyValues(columns_name)
            dataframe.columns = columns_name
            return dataframe

    def getEquivalentColumns(self, wrapper_table):
        columns_name = wrapper_table.getNameColumns()
        equivalent_columns = {col:[col] for col in columns_name}
        return equivalent_columns


    # Create a dataframe with empty values
    def getDataframeWithEmptyValues(self, columns_name):
        dataframe = pd.DataFrame(np.array([[0,"2000-01-01", 0, "alimentaire", "course", "walmart", "courses", None, "carte", 0]]),
                    columns=columns_name)
        return dataframe 


        
class ResponseSqlToList():
    def translateResponseSqlToList(self, response_sql):
        list_response = [elem[0] for elem in response_sql]
        return list_response