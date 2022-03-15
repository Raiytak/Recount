from dash import callback
import logging

from recount_tools import getUsername, getIdButtonClicked

from pipeline.pipeline import DataPipeline, GraphPipeline

from .abstract_mixin import AbstractAction

from .import_excel import saveImportedFile

import website.vue.graphs as graphs
from pipeline.convert import convertPeriodToDate, shapeDatetimeToSimpleDate


class DashboardMixin(AbstractAction):
    def setCallbacks(self):
        # TODO: graph colors should be the same
        @callback(*self.osi_update_graphs)
        def update_graphs(
            selected_date, selected_period, imported_excel, conf_submited
        ):
            return self.updateGraph(
                selected_date, selected_period, imported_excel, conf_submited
            )

        @callback(*self.osi_reset_button_pressed)
        def reset_button_pressed(nclicks):
            return self.reset_button_pressed(nclicks)

        # @callback(*self.osi_confirm_reset)
        # def confirm_reset(conf_submited):
        #     return self.confirm_reset(conf_submited)

    @staticmethod
    def updateGraph(selected_date, selected_period, imported_excel, conf_submited):
        username = getUsername()
        data_pipeline = DataPipeline(username)
        graph_pipeline = GraphPipeline(username)
        id_component_called = getIdButtonClicked()

        if conf_submited:
            data_pipeline.user_files.removeUserFolder()
            data_pipeline.dumpUserOfAllTables()
            return (
                {},
                {},
                {},
                {},
                "Your data has been reset!",
            )

        if "import" in id_component_called:
            saveImportedFile(username, imported_excel)
            DashboardMixin.updateDataForUser(username)
            logging.info("Data has been updated successfully!")

        end_datetime = convertPeriodToDate(selected_date, selected_period)
        end_date = shapeDatetimeToSimpleDate(end_datetime)
        dataframe = graph_pipeline.getExpenseRepaidForPeriod(selected_date, end_date)

        main_category_df = dataframe.copy()
        main_category_df["category"] = main_category_df["category"].apply(
            func=graph_pipeline.selectMainCategory
        )

        list_dict_of_expenses = graph_pipeline.getDataByColumn(main_category_df)
        scatter_graph = graphs.scatterGraph(
            list_dict_of_expenses, [selected_date, end_date]
        )

        list_dict_of_sum_expenses = graph_pipeline.getSumDataByColumn(main_category_df)
        pie_graph = graphs.pieGraph(list_dict_of_sum_expenses)

        expenses_by_period = graph_pipeline.getDataByDateDeltaAndColumn(
            main_category_df
        )
        mean_graph = graphs.meanGraph(expenses_by_period)

        # TODO: improve stability by defining default categories, imposed categories ?
        food_dataframe = dataframe[main_category_df["category"] == "alimentary"].copy()
        food_dataframe["category"] = food_dataframe["category"].apply(
            func=graph_pipeline.selectSecondCategory
        )
        food_by_period = graph_pipeline.getDataByDateDeltaAndColumn(food_dataframe)
        food_graph = graphs.meanGraph(food_by_period)

        return scatter_graph, pie_graph, mean_graph, food_graph, None

    @property
    def osi_update_graphs(self):
        outputs = self.recount_graphs.dashboardHomeCallbacks() + [
            self.recount_outputs.resetUserDataOutputCallback()
        ]
        rec_in = self.recount_inputs
        inputs = (
            rec_in.dateCallback(),
            rec_in.periodCallback(),
            rec_in.importExcelCallback(),
            self.recount_inputs.confirmDialogueInput(self.reset_dial),
        )
        return (outputs, inputs)

    @staticmethod
    def reset_button_pressed(nclicks):
        if nclicks:
            return True
        return False

    @property
    def osi_reset_button_pressed(self):
        return (
            self.recount_outputs.confirmDialogueOutput(self.reset_dial),
            self.recount_inputs.resetUserDataButtonCallback(),
        )

        # @staticmethod
        # def confirm_reset(conf_submited):
        #     if conf_submited:
        #         username = getUsername()
        #         data_pipeline = DataPipeline(username)
        #         data_pipeline.user_files.removeUserFolder()
        #         data_pipeline.dumpUserOfAllTables()
        #         return "Your data has been reset.\nYou can refresh the page!"

        # @property
        # def osi_confirm_reset(self):
        #     return (
        #         self.recount_outputs.resetUserDataOutputCallback(),
        #         self.recount_inputs.confirmDialogueInput(self.reset_dial),
        #     )

        # def export_or_reset_data(reset_nclicks, export_nclicks):
        #     id_component_called = getIdButtonClicked()
        #     if "reset" in id_component_called:
        #         return True  # , None
        # elif "export" in id_component_called:
        #     username = getUsername()
        #     myAccessUserFiles = AccessUserFiles(username)
        #     path_excel = myAccessUserFiles.AccessExcel.ExcelPaths.rawExcelPath()
        #     myExcelToDataframe = ExcelToDataframe(username)
        #     df_excel = myExcelToDataframe.getDataframeOf(path_excel)

        #     def delete_df_unnamed_col(df):
        #         for col in df.columns:
        #             if "Unnamed" in col:
        #                 del df[col]

        #     delete_df_unnamed_col(df_excel)
        #     excel_exported = dcc.send_data_frame(
        #         df_excel.to_excel, "recount_excel.xlsx", sheet_name="Sheet_name_1"
        #     )
        #     return False, excel_exported
        #     # return False, None
        return False  # , None

    @staticmethod
    def updateDataForUser(username):
        update_data = DataPipeline(username)
        update_data.updateData()

