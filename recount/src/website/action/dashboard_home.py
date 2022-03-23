import logging
from dash import callback, dcc, Input, Output, State

from recount_tools import getUsername, getIdButtonClicked

from pipeline.pipeline import DataPipeline, GraphPipeline

from .abstract_mixin import AbstractAction

from .graphs import *
from pipeline.convert import convertPeriodToDate, shapeDatetimeToSimpleDate

__all__ = ["DashboardHomeMixin"]


class DashboardHomeMixin(AbstractAction):
    def setCallbacks(self):
        @callback(*self.osi_update_data, prevent_initial_call=True)
        def update_data(*args):
            return self.update_data(*args)

        # TODO: graph colors should be the same
        @callback(*self.osi_update_graphs)
        def update_graphs(*args):
            return self.update_graphs(*args)

        @callback(*self.osi_reset_button_pressed, prevent_initial_call=True)
        def reset_button_pressed(reset_nclicks):
            return self.reset_button_pressed(reset_nclicks)

        @callback(*self.osi_download_button_pressed, prevent_initial_call=True)
        def download_button_pressed(*args):
            return self.download_button_pressed(*args)

    @property
    def osi_update_graphs(self):
        return (
            self.dashboard_home.dashboardHomeCallbacks(),
            Input(self.dashboard_home.date_div_date_id, "date"),
            Input(self.dashboard_home.date_div_period_id, "value"),
            Input(self.dashboard_home.update_graph_button, "n_clicks"),
        )

    @staticmethod
    def update_graphs(selected_date, selected_period, refresh):
        username = getUsername()
        graph_pipeline = GraphPipeline(username)

        end_datetime = convertPeriodToDate(selected_date, selected_period)
        end_date = shapeDatetimeToSimpleDate(end_datetime)
        dataframe = graph_pipeline.getExpenseRepaidForPeriod(selected_date, end_date)

        main_category_df = dataframe.copy()
        main_category_df["category"] = main_category_df["category"].apply(
            func=graph_pipeline.selectMainCategory
        )

        list_dict_of_expenses = graph_pipeline.getDataByColumn(main_category_df)
        scatter_graph = scatterGraph(list_dict_of_expenses, [selected_date, end_date])

        list_dict_of_sum_expenses = graph_pipeline.getSumDataByColumn(main_category_df)
        pie_graph = pieGraph(list_dict_of_sum_expenses)

        expenses_by_period = graph_pipeline.getDataByDateDeltaAndColumn(
            main_category_df
        )
        mean_graph = meanGraph(expenses_by_period)

        # TODO: improve stability by defining default categories, imposed categories ?
        food_dataframe = dataframe[main_category_df["category"] == "alimentary"].copy()
        food_dataframe["category"] = food_dataframe["category"].apply(
            func=graph_pipeline.selectSecondCategory
        )
        food_by_period = graph_pipeline.getDataByDateDeltaAndColumn(food_dataframe)
        food_graph = meanGraph(food_by_period)

        return scatter_graph, pie_graph, mean_graph, food_graph

    @property
    def osi_reset_button_pressed(self):
        return (
            Output(self.dashboard_home.confirm_reset_dialogue, "displayed"),
            Input(self.dashboard_home.reset_button, "n_clicks"),
        )

    @staticmethod
    def reset_button_pressed(reset_nclicks):
        if reset_nclicks:
            return True
        return False

    @property
    def osi_update_data(self):
        return (
            Output(self.dashboard_home.update_graph_button, "n_clicks"),
            Input(self.dashboard_home.update_data_button, "n_clicks"),
            Input(self.dashboard_home.upload_excel, "contents"),
            Input(self.dashboard_home.confirm_reset_dialogue, "submit_n_clicks"),
            State(self.dashboard_home.update_graph_button, "n_clicks"),
        )

    @staticmethod
    def update_data(
        refresh, imported_excel, reset_confirmed, graph_button_status,
    ):
        button_clicked = getIdButtonClicked()
        username = getUsername()
        user_data = DataPipeline(username)

        if "upload-excel" in button_clicked:
            if imported_excel != None:
                logging.info(f"{username}: Importing file ...")
                user_data.user_files.saveImportedFile(imported_excel)
                logging.info(f"{username}: File imported!")

        elif "confirm-reset-dialog" in button_clicked:
            logging.info("Reseting data of '{}' ...".format(username))
            user_data.user_files.removeUserFolder()
            user_data.dumpUserOfAllTables()
            logging.info("Data of '{}' is reseted".format(username))
            return graph_button_status + 1

        user_data.updateData()

        return graph_button_status + 1

    @property
    def osi_download_button_pressed(self):
        return (
            Output(self.dashboard_home.download_excel, "data"),
            Input(self.dashboard_home.download_excel_button, "n_clicks"),
        )

    @staticmethod
    def download_button_pressed(export_nclicks):
        username = getUsername()
        user_data = DataPipeline(username)
        df = user_data.getDataframeFromExcel()
        return dcc.send_data_frame(
            df.to_excel, "recount_excel.xlsx", sheet_name="Sheet_name_1"
        )
