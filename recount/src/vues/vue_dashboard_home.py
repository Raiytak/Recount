import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import update_data

from accessors.access_files import AccessUserFiles

from wrapper_dash.reusable_components.reusable_inputs import ReusableInputs
from wrapper_dash.reusable_components.reusable_outputs import ReusableOutputs
from wrapper_dash.reusable_components.reusable_graphs import ReusableGraphs
from wrapper_dash.reusable_components.reusable_links import ReusableLinks

from wrapper_dash.facilitator_dash.tools import getUsername, getIdButtonClicked
from wrapper_dash.facilitator_dash.date_to_dataframe import DateToDataframe
from wrapper_dash.facilitator_dash.convert_df_to_graph import DataframeToGraph
from wrapper_dash.facilitator_dash.import_excel import ImportExcelFileSaver

from wrapper_excel.excel_to_df import ExcelToDataframe

from accessors.access_files import AccessUserFiles


class ElementsVue:
    def __init__(self, ReusableInputs, ReusableOutputs, ReusableGraphs):
        self.ReusableInputs = ReusableInputs
        self.ReusableOutputs = ReusableOutputs
        self.ReusableGraphs = ReusableGraphs

        (
            self.output_conf,
            self.input_conf,
        ) = self.ReusableOutputs.getConfirmDialogueCallbacks()

    def getInputDiv(self):
        return self.ReusableInputs.getDashboardInputsDiv()

    def getInputCallbacks(self):
        return self.ReusableInputs.getDatePeriodAndExcelCallbacks()

    def getGraphDiv(self):
        return self.ReusableGraphs.getDashboardHomeDiv()

    def getGraphCallbacks(self):
        return self.ReusableGraphs.getlDashboardHomeCallbacks()

    def getOutputTypeDivs(self):
        return self.ReusableGraphs.getDashboardHomeTypeGraphs()

    def getExportResetExcelCallbacks(self):
        return self.ReusableInputs.getExportResetExcelCallbacks()

    def getConfirmDialogueInputCallback(self):
        output_conf, input_conf = self.ReusableOutputs.getConfirmDialogueCallbacks()
        return input_conf

    def getConfirmDialogueOutputCallback(self):
        output_conf, input_conf = self.ReusableOutputs.getConfirmDialogueCallbacks()
        return output_conf


class EmptyVue:
    def __init__(self):
        self.name_vue = "dashboard-home-"
        self.ReusableInputs = ReusableInputs(self.name_vue)
        self.ReusableOutputs = ReusableOutputs(self.name_vue)
        self.ReusableGraphs = ReusableGraphs(self.name_vue)
        self.ReusableLinks = ReusableLinks()
        self.ElementsVue = ElementsVue(
            self.ReusableInputs, self.ReusableOutputs, self.ReusableGraphs
        )

    def getEmptyVue(self):
        conf_dial = self.ReusableOutputs.getConfirmDialogue()

        upper_div = self.ElementsVue.getInputDiv()
        dashboard_div = self.ElementsVue.getGraphDiv()
        dashboard = html.Div([upper_div, dashboard_div])

        hidden_vue = self.ReusableOutputs.getHiddenDiv("reset-button")

        total_vue = html.Div([dashboard, hidden_vue, conf_dial])

        return total_vue

    def getInputCallbacks(self):
        input_callbacks = self.ElementsVue.getInputCallbacks()
        return input_callbacks

    def getExportResetExcelCallbacks(self):
        return self.ElementsVue.getExportResetExcelCallbacks()

    def getResetExportConfirmInputCallback(self):
        return self.ElementsVue.getConfirmDialogueInputCallback()

        # rec_callbacks.append(self.ReusableOutputs.getHiddenDivCallback("reset-button"))

    def getResetButtonOutputCallback(self):
        return self.ReusableOutputs.getHiddenDivCallback("reset-button")

    def getOutputCallbacks(self):
        return self.ElementsVue.getGraphCallbacks()

    def getOutputTypesDiv(self):
        return self.ElementsVue.getOutputTypeDivs()

    def getResetExportConfirmOutputCallbacks(self):
        confirm_output = self.ElementsVue.getConfirmDialogueOutputCallback()
        export_excel_output = self.ReusableInputs.getExportExcelOutputCallback()
        return [confirm_output, export_excel_output]


# Dash Application
class AppDash(EmptyVue):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.DateToDataframe = DateToDataframe()
        self.ConvertDfToGraph = DataframeToGraph()
        self.ImportExcelFileSaver = ImportExcelFileSaver()

        self.setCallback()

    def setCallback(self):
        @self.app.callback(self.getOutputCallbacks(), self.getInputCallbacks())
        def update_graph(selected_date_str, selected_periode, imported_excel):
            username = getUsername()
            id_component_called = getIdButtonClicked()
            if "import" in id_component_called:
                self.ImportExcelFileSaver.saveImportedFile(username, imported_excel)
                update_data.updateAll(username)

            dataframe, range_date = self.DateToDataframe.getDataframeFromDate(
                username, selected_date_str, selected_periode
            )
            list_dataframes = self.DateToDataframe.getListDataframeByWeekFromDate(
                username, selected_date_str, selected_periode
            )

            list_types_of_divs = self.getOutputTypesDiv()

            scatter_graph = self.ConvertDfToGraph.convertDataframeToGraph(
                dataframe, list_types_of_divs[0], range_date
            )
            pie_graph = self.ConvertDfToGraph.convertDataframeToGraph(
                dataframe, list_types_of_divs[1]
            )
            mean_graph = self.ConvertDfToGraph.convertDataframeToGraph(
                list_dataframes, list_types_of_divs[2], range_date
            )
            food_graph = self.ConvertDfToGraph.convertDataframeToGraph(
                list_dataframes, list_types_of_divs[3], range_date
            )

            return scatter_graph, pie_graph, mean_graph, food_graph

        @self.app.callback(
            self.getResetExportConfirmOutputCallbacks(),
            self.getExportResetExcelCallbacks(),
        )
        def export_or_reset_data(reset_nclicks, export_nclicks):
            id_component_called = getIdButtonClicked()
            if "reset" in id_component_called:
                return True, None
            elif "export" in id_component_called:
                username = getUsername()
                myAccessUserFiles = AccessUserFiles(username)
                path_excel = myAccessUserFiles.AccessExcel.ExcelPaths.rawExcelPath()
                myExcelToDataframe = ExcelToDataframe(username)
                df_excel = myExcelToDataframe.getDataframeOf(path_excel)

                def delete_df_unnamed_col(df):
                    for col in df.columns:
                        if "Unnamed" in col:
                            del df[col]

                delete_df_unnamed_col(df_excel)
                excel_exported = dcc.send_data_frame(
                    df_excel.to_excel, "recount_excel.xlsx", sheet_name="Sheet_name_1"
                )
                return False, excel_exported
                # return False, None
            return False, None

        @self.app.callback(
            self.getResetButtonOutputCallback(),
            self.getResetExportConfirmInputCallback(),
        )
        def confirm_reset(conf_dial_submited):
            username = getUsername()
            myAccessUserFiles = AccessUserFiles(username)

            if conf_dial_submited != None:
                myAccessUserFiles.removeExcelsOfUser()
                update_data.removeAllDataForUser(username)
            return ""

    def setThisVue(self):
        return self.getEmptyVue()
