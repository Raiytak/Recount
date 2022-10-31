import logging
from datetime import datetime
from dash import callback, dcc, Input, Output, State

from .tools import *
from .abstract_mixin import AbstractAction
from .graphs import *
from pipeline.pipeline import cleanDf

__all__ = ["DashboardMixin"]


class DashboardMixin(AbstractAction):
    def __init__(
        self,
        table,
        classUserManager,
        classExcelManager,
        classUserSqlTable,
        classDatabaseManager,
        classDashManager,
        *args,
        **kwargs,
    ):
        self.table = table
        self.classUserManager = classUserManager
        self.classExcelManager = classExcelManager
        self.classUserSqlTable = classUserSqlTable
        self.classDatabaseManager = classDatabaseManager
        self.classDashManager = classDashManager
        super().__init__(*args, **kwargs)

    def instanciateManagers(self) -> tuple:
        username = getUsername()
        user_manager = self.classUserManager(username)
        excel_manager = self.classExcelManager(user_manager)
        sql_table = self.classUserSqlTable(username, self.table)
        db_manager = self.classDatabaseManager(sql_table)
        dash_manager = self.classDashManager(excel_manager)
        return excel_manager, db_manager, dash_manager

    def setCallbacks(self):

        # TODO: graph colors should be the same
        @callback(*self.io_update_graphs)
        def update_graphs(*args):
            return self.update_graphs(*args)

        @callback(*self.io_reset_button_pressed, prevent_initial_call=True)
        def reset_button_pressed(reset_nclicks):
            return self.reset_button_pressed(reset_nclicks)

        @callback(*self.io_update_data, prevent_initial_call=True)
        def update_data(*args):
            return self.update_data(*args)

        @callback(*self.io_download_button_pressed, prevent_initial_call=True)
        def download_button_pressed(*args):
            return self.download_button_pressed(*args)

    @property
    def io_update_graphs(self):
        return (
            self.dashboard_home.dashboardCallbacks(),
            Input(self.dashboard_home.date_div_date_id, "date"),
            Input(self.dashboard_home.date_div_period_id, "value"),
            Input(self.dashboard_home.update_graph_button, "n_clicks"),
        )

    def update_graphs(self, selected_date, selected_period, refresh):
        _, db_manager, dash_manager = self.instanciateManagers()

        username = getUsername()
        logging.info("@{}: Refresing graph ...".format(username))

        start_date = datetime.strptime(selected_date, "%Y-%m-%d")
        end_date = addDeltaToDatetime(start_date, selected_period)
        range_date = [start_date, end_date]
        df = db_manager.dataframe(start_date, end_date)

        dash_manager.cleanDf(df)
        expenses = dash_manager.expensesByCategory(df)
        scatter_graph = scatterGraph(expenses, [selected_date, end_date])

        sum_expenses = dash_manager.sumExpensesByCategory(df)
        pie_graph = pieGraph(sum_expenses)

        expenses_by_period = dash_manager.sumExpensesByCategoryByPeriod(
            df, selected_period
        )
        mean_graph = meanGraph(expenses_by_period, range_date)

        alimentary_by_period = dash_manager.sumExpensesAlimentaryByPeriod(
            df, selected_period
        )
        food_graph = meanGraph(alimentary_by_period, range_date)

        logging.info("@{}: Graph refreshed!".format(username))

        return scatter_graph, pie_graph, mean_graph, food_graph

    @property
    def io_reset_button_pressed(self):
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
    def io_update_data(self):
        return (
            Output(self.dashboard_home.update_graph_button, "n_clicks"),
            Output(self.dashboard_home.loading_div, "children"),
            Input(self.dashboard_home.update_data_button, "n_clicks"),
            Input(self.dashboard_home.upload_excel, "contents"),
            Input(self.dashboard_home.confirm_reset_dialogue, "submit_n_clicks"),
            State(self.dashboard_home.update_graph_button, "n_clicks"),
        )

    def update_data(
        self, refresh, imported_excel, reset_confirmed, graph_button_status,
    ):
        button_clicked = getIdButtonClicked()
        excel_manager, db_manager, dash_manager = self.instanciateManagers()
        username = getUsername()
        if "upload-excel" in button_clicked:
            if imported_excel != None:
                logging.info(f"{username}: Uploading file ...")
                excel_manager.saveImportedExcel(imported_excel)
                logging.info(f"{username}: File uploaded!")

        elif "confirm-reset-dialog" in button_clicked:
            logging.info("@{}: Reseting data ...".format(username))
            excel_manager.user_manager.removeAllExcels()
            db_manager.user_table.truncateUserOfTable()
            logging.info("@{}: Data is reseted!".format(username))
            return graph_button_status + 1, None

        logging.info(f"{username}: Update data on database ...")
        df = excel_manager.dataframe()
        cleaned_df = cleanDf(df, False)
        db_manager.user_table.truncateUserOfTable()
        db_manager.saveDataframe(cleaned_df)
        logging.info(f"{username}: Update done!")

        return graph_button_status + 1, None

    @property
    def io_download_button_pressed(self):
        return (
            Output(self.dashboard_home.download_excel, "data"),
            Input(self.dashboard_home.button_download_excel, "n_clicks"),
        )

    def download_button_pressed(self, export_nclicks):
        excel_manager, _, _ = self.instanciateManagers()
        df = excel_manager.dataframe()
        return dcc.send_data_frame(
            df.to_excel,
            "recount_excel.xlsx",
            sheet_name="Sheet_name_1",
            # index=None, # TODO: remove index from excel
        )
