import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


import update_db
import communication_db
DateToDataframe = communication_db.DateToDataframe()


# Import the config file
import config.access_config as access_config
myAccessConfig = access_config.AccessConfig()
config_json = myAccessConfig.getConfig()

# Get the different paths used in the app
import wrapper_excel.paths_docs as paths_docs
TSTAuthPath = paths_docs.ThemesAndSubthemesAuthorized(config_json)
ExcelPath = paths_docs.ExcelPath(config_json)

import wrapper_excel.access_docs as access_docs
accessAuthorizedTST = access_docs.AccessTSTAuthorized(TSTAuthPath)
authorizedTST_json = accessAuthorizedTST.getJson()


# Objects used to clean the data
# import wrapper_dash.facilitator_dash.prepare_dashboard as prepare_dashboard
import wrapper_dash.facilitator_dash.main_convert_df_to_graph as main_convert_df_to_graph
import wrapper_dash.facilitator_dash.convert_ld_to_graph as convert_ld_to_graph
import wrapper_dash.facilitator_dash.convert_df_to_ld as convert_df_to_ld
DataframeToListDict = convert_df_to_ld.DataframeToListOfDicts()
ListDictToGraph = convert_ld_to_graph.ListDictToGraph(authorizedTST_json)
ConvertDfToGraph = main_convert_df_to_graph.DataframeToGraph(DataframeToListDict, ListDictToGraph)

# Object used to import an excel given by the user
import wrapper_dash.facilitator_dash.import_excel as import_excel
FileSaver = import_excel.FileSaver(ExcelPath)   





from wrapper_dash import vue_index, vue_home
from wrapper_dash import vue_dashboard_home, vue_modify_themes_file


# Dash Application
class AppDash():
    def __init__(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

        self.vueIndex = vue_index.AppDash(self.app)
        self.vueHome = vue_home.AppDash(self.app)
        self.vueDashboardHome = vue_dashboard_home.AppDash(self.app, DateToDataframe, ConvertDfToGraph, FileSaver)
        self.vueThemesFile = vue_modify_themes_file.AppDash(self.app, accessAuthorizedTST)
    


    def setVueIndex(self):
        self.app.layout = self.vueIndex.setThisEmptyDefaultVue()

    # You can add a vue by inserting the desirated vue and path here
    def setCallback(self):
        @self.app.callback(Output('default-page-content', 'children'),
                    Input('default-url', 'pathname'))
        def display_page(pathname):
            if pathname == '/' and len(pathname) == 1:
                return self.vueIndex.setThisVue()
            if pathname == '/home':
                return self.vueHome.setThisVue()
            if pathname == '/dashhome':
                return self.vueDashboardHome.setThisVue()
            elif pathname == '/themes':
                return self.vueThemesFile.setThisVue()
            else:
                return '404'
            pass


    
    def launch(self):
        self.setVueIndex()
        self.setCallback()
        print("-#- Application Running -#-\n")
        self.run()
    def run(self):
        self.app.run_server(debug=True)
        