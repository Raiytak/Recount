import dash
from dash.dependencies import Input, Output


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

# Access the documents, to get the value and update those. Need the paths to work.
import accessors.access_docs as access_docs
myAccessExcel = access_docs.AccessExcel(myExcelPath)
<<<<<<< HEAD
accessAuthorizedTST = access_docs.AccessTSTAuthorized(TSTAuthPath)
authorizedTST_json = accessAuthorizedTST.getJson()
=======
myAccessCTAuthorized = access_docs.AccessCTAuthorized(myCatThemeAuthPath)
authorizedCT_json = myAccessCTAuthorized.getJson()

>>>>>>> e970bffec6e60a935dbe260042bf627c10034e6f

# Objects used to clean and convert the data into dataframe and objects readable for the dash app
# import wrapper_dash.facilitator_dash.prepare_dashboard as prepare_dashboard
import wrapper_dash.facilitator_dash.main_convert_df_to_graph as main_convert_df_to_graph
import wrapper_dash.facilitator_dash.convert_ld_to_graph as convert_ld_to_graph
import wrapper_dash.facilitator_dash.convert_df_to_ld as convert_df_to_ld
DataframeToListDict = convert_df_to_ld.DataframeToListOfDicts()
ListDictToGraph = convert_ld_to_graph.ListDictToGraph(authorizedCT_json)
ConvertDfToGraph = main_convert_df_to_graph.DataframeToGraph(DataframeToListDict, ListDictToGraph)

# Object used to save an excel uploaded by the user
import wrapper_dash.facilitator_dash.import_excel as import_excel
FileSaver = import_excel.FileSaver(myAccessExcel)   



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
        self.vueThemesFile = vue_modify_themes_file.AppDash(self.app, myAccessCTAuthorized)
    


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
        