import dash
import dash_auth
from dash.dependencies import Input, Output

import update_db

import communication_db_user

DateToDataframe = communication_db_user.DateToDataframe()


# Import the config file
from accessors.access_config import AccessConfig

myAccessConfig = AccessConfig()
import accessors.access_users as access_users

myAccessUsers = access_users.AccessUsers()

# Access the documents, to get the values, dataframe and update the docs. Need the paths to work.
from accessors.access_files import AccessCTAuthorized


myAccessCTAuthorized = AccessCTAuthorized()
authorizedCT_json = myAccessCTAuthorized.getJson()


# Objects used to clean and convert the data into dataframe and objects readable for the dash app
# import wrapper_dash.facilitator_dash.prepare_dashboard as prepare_dashboard
from wrapper_dash.facilitator_dash.convert_df_to_ld import DataframeToListOfDicts

DataframeToListDict = DataframeToListOfDicts()
from wrapper_dash.facilitator_dash.convert_ld_to_graph import ListDictToGraph

ListDictToGraph = ListDictToGraph(authorizedCT_json)
from wrapper_dash.facilitator_dash.main_convert_df_to_graph import DataframeToGraph

ConvertDfToGraph = DataframeToGraph(DataframeToListDict, ListDictToGraph)

# Object used to save an excel uploaded by the user
from wrapper_dash.facilitator_dash.import_excel import ImportExcelFileSaver

ImportExcelFileSaver = ImportExcelFileSaver(update_db)

from wrapper_dash.facilitator_dash.save_config import (
    ConfigNotebookExcelSaver,
    StandardButtonsConfigSaver,
)

ConfigNotebookExcelSaver = ConfigNotebookExcelSaver()
StandardButtonsConfigSaver = StandardButtonsConfigSaver()


from wrapper_dash import vue_index, vue_home
from wrapper_dash import vue_dashboard_home
from wrapper_dash import vue_test

import wrapper_dash.facilitator_dash.user_identification as user_identification


# Dash Application
class AppDash:
    def __init__(self):
        external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
        self.app = dash.Dash(
            __name__,
            external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=True,
        )
        self.setAuthentification()

        self.vueIndex = vue_index.AppDash(self.app)
        self.vueHome = vue_home.AppDash(self.app)
        self.vueDashboardHome = vue_dashboard_home.AppDash(
            self.app, DateToDataframe, ConvertDfToGraph, ImportExcelFileSaver
        )

        self.vueTest = vue_test.AppDash(self.app)

    def setVueIndex(self):
        self.app.layout = self.vueIndex.setThisEmptyDefaultVue()

    # You can add a vue by inserting the desirated vue and path here
    def setCallback(self):
        @self.app.callback(
            Output("default-page-content", "children"), Input("default-url", "pathname")
        )
        def display_page(pathname):
            username = user_identification.getUsername()
            dash.callback_context.response.set_cookie("username", username)

            if pathname == "/" and len(pathname) == 1:
                return self.vueIndex.setThisVue()
            elif pathname == "/home":
                return self.vueHome.setThisVue()
            elif pathname == "/dashhome":
                update_db.updateAll(username)
                return self.vueDashboardHome.setThisVue()
            elif pathname == "/test":
                return self.vueTest.setThisVue()
            else:
                return "404 Page not found."
            pass

    def launch(self):
        self.setVueIndex()
        self.setCallback()
        # print(f"-#- Request from '{username}' -#-\n")
        self.run()

    def run(self):
        self.app.run_server(debug=True)

    def setAuthentification(self):
        VALID_USERNAME_PASSWORD_PAIRS = myAccessUsers.getUsers()
        dash_auth.BasicAuth(self.app, VALID_USERNAME_PASSWORD_PAIRS)


# --- MAIN PART ---
if __name__ == "__main__":
    # --- INIT ---
    print("-#- Application Running -#-\n")
    myApp = AppDash()
    myApp.launch()
