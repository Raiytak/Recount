from src.logs import formatAndDisplay
from src.pipeline.pipeline import DataPipeline, GraphPipeline

from .abstract_mixin import AbstractAction
from recount_tools import getUsername, getIdButtonClicked

from .import_excel import saveImportedFile

import src.website.vue.graphs as graphs
from src.pipeline.convert import convertPeriodToDate, shapeDatetimeToSimpleDate


class DashboardMixin(AbstractAction):
    def setCallbacks(self):
        outputs = [out_call for out_call in self.output_callbacks.values()]
        inputs = [
            in_call for key, in_call in self.input_callbacks.items() if key != "reset"
        ]

        @self.app.callback(outputs, inputs)
        def update_graph(
            selected_date, selected_period, imported_excel,
        ):
            username = getUsername()
            graph_pipeline = GraphPipeline(username)
            id_component_called = getIdButtonClicked()

            if "import" in id_component_called:
                saveImportedFile(username, imported_excel)
                DashboardMixin.updateDataForUser(username)
                formatAndDisplay(f"{username}: Data update done")

            end_datetime = convertPeriodToDate(selected_date, selected_period)
            end_date = shapeDatetimeToSimpleDate(end_datetime)
            dataframe = graph_pipeline.getDataframeForPeriod(selected_date, end_date)

            main_category_df = dataframe.copy()
            main_category_df["category"] = main_category_df["category"].apply(
                func=graph_pipeline.selectMainCategory
            )

            list_dict_of_expenses = graph_pipeline.getDataByColumn(main_category_df)
            scatter_graph = graphs.scatterGraph(
                list_dict_of_expenses, [selected_date, end_date]
            )

            list_dict_of_sum_expenses = graph_pipeline.getSumDataByColumn(
                main_category_df
            )
            pie_graph = graphs.pieGraph(list_dict_of_sum_expenses)

            expenses_by_period = graph_pipeline.getDataByDateDeltaAndColumn(
                main_category_df
            )
            mean_graph = graphs.meanGraph(expenses_by_period)

            # TODO: improve
            food_dataframe = dataframe[
                main_category_df["category"] == "alimentary"
            ].copy()
            food_dataframe["category"] = food_dataframe["category"].apply(
                func=graph_pipeline.selectSecondCategory
            )
            food_by_period = graph_pipeline.getDataByDateDeltaAndColumn(food_dataframe)
            food_graph = graphs.meanGraph(food_by_period)

            return scatter_graph, pie_graph, mean_graph, food_graph

        # @self.app.callback([outputs[0]], self.input_callbacks)
        # def confirm_reset(conf_dial_submited):
        #     username = getUsername()
        #     myAccessUserFiles = AccessUserFiles(username)

        #     if conf_dial_submited != None:
        #         myAccessUserFiles.removeExcelsOfUser()
        #         update_data.removeAllDataForUser(username)
        #     return ""

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

    @staticmethod
    def updateDataForUser(username):
        update_data = DataPipeline(username)
        update_data.updateData()

