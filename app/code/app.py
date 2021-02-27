import dash
from dash.dependencies import Input, Output

import update_db

import communication_db
DateToDataframe = communication_db.DateToDataframe()


# Import the config file
import accessors.access_config as access_config
myAccessConfig = access_config.AccessConfig()
config_json = myAccessConfig.getConfig()

# Get the different paths of the files used in the app.
import accessors.paths_docs as paths_docs
myExcelPath = paths_docs.ExcelPath(config_json)
myCatThemeAuthPath = paths_docs.CategoryAndThemeAuthorizedPath(config_json)
myNotebookExcelConfigPath = paths_docs.NotebookConfigPath(config_json)
myStandardButtonsConfigPath = paths_docs.StandardButtonsConfigPath(config_json)

# Access the documents, to get the values, dataframe and update the docs. Need the paths to work.
import accessors.access_docs as access_docs
myAccessExcel = access_docs.AccessExcel(myExcelPath)
myAccessCTAuthorized = access_docs.AccessCTAuthorized(myCatThemeAuthPath)
myAccessNotebookExcelConfig = access_docs.AccessNotebookConfig(myNotebookExcelConfigPath)
myAccessStandardButtonsConfig = access_docs.AccessStandardButtonsConfig(myStandardButtonsConfigPath)
authorizedCT_json = myAccessCTAuthorized.getJson()

import wrapper_excel.convert_excel_to_df as convert_excel_to_df
myExcelToDataframe = convert_excel_to_df.ExcelToDataframe(myAccessExcel)


# Objects used to clean and convert the data into dataframe and objects readable for the dash app
# import wrapper_dash.facilitator_dash.prepare_dashboard as prepare_dashboard
import wrapper_dash.facilitator_dash.convert_df_to_ld as convert_df_to_ld
DataframeToListDict = convert_df_to_ld.DataframeToListOfDicts()
import wrapper_dash.facilitator_dash.convert_ld_to_graph as convert_ld_to_graph
ListDictToGraph = convert_ld_to_graph.ListDictToGraph(authorizedCT_json)
import wrapper_dash.facilitator_dash.main_convert_df_to_graph as main_convert_df_to_graph
ConvertDfToGraph = main_convert_df_to_graph.DataframeToGraph(DataframeToListDict, ListDictToGraph)

# Object used to save an excel uploaded by the user
import wrapper_dash.facilitator_dash.import_excel as import_excel
ImportExcelFileSaver = import_excel.ImportExcelFileSaver(myExcelToDataframe, update_db)    

import wrapper_dash.facilitator_dash.save_config as save_config
ConfigNotebookExcelSaver = save_config.ConfigNotebookExcelSaver(myAccessNotebookExcelConfig) 
StandardButtonsConfigSaver = save_config.StandardButtonsConfigSaver(myAccessStandardButtonsConfig)     



from wrapper_dash import vue_index, vue_home
from wrapper_dash import vue_dashboard_home, vue_modify_categories_file
from wrapper_dash import vue_notebook_excel


# Dash Application
class AppDash():
    def __init__(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

        self.vueIndex = vue_index.AppDash(self.app)
        self.vueHome = vue_home.AppDash(self.app)
        self.vueDashboardHome = vue_dashboard_home.AppDash(self.app, DateToDataframe, ConvertDfToGraph, ImportExcelFileSaver)
        self.vueCategoriesFile = vue_modify_categories_file.AppDash(self.app, myAccessCTAuthorized, StandardButtonsConfigSaver)

        self.vueNotebookExcel = vue_notebook_excel.AppDash(self.app, myExcelToDataframe, ImportExcelFileSaver, ConfigNotebookExcelSaver, StandardButtonsConfigSaver)
    


    def setVueIndex(self):
        self.app.layout = self.vueIndex.setThisEmptyDefaultVue()

    # You can add a vue by inserting the desirated vue and path here
    def setCallback(self):
        @self.app.callback(Output('default-page-content', 'children'),
                    Input('default-url', 'pathname'))
        def display_page(pathname):
            if pathname == '/' and len(pathname) == 1:
                return self.vueIndex.setThisVue()
            elif pathname == '/home':
                return self.vueHome.setThisVue()
            elif pathname == '/dashhome':
                return self.vueDashboardHome.setThisVue()
            elif pathname == '/categories':
                return self.vueCategoriesFile.setThisVue()
            elif pathname == '/excel':
                return self.vueNotebookExcel.setThisVue()
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
        