import logging
from dash import callback, html, dcc, Input, Output, State

from .tools import *

from .abstract_mixin import AbstractAction

from src.web.vue.components.css_style import *
from .graphs import *
from .tools import *

__all__ = ["HomeMixin"]


class HomeMixin(AbstractAction):
    def __init__(
        self, classUserManager, classExcelManager, *args, **kwargs,
    ):
        self.classUserManager = classUserManager
        self.classExcelManager = classExcelManager
        super().__init__(*args, **kwargs)

    def instanciateManagers(self):
        username = getUsername()
        user_manager = self.classUserManager(username)
        excel_manager = self.classExcelManager(user_manager)
        return excel_manager

    def setCallbacks(self):
        @callback(*self.io_download_button_pressed)
        def download_button_pressed(*args):
            return self.download_button_pressed(*args)

    @property
    def io_download_button_pressed(self):
        return (
            Output(self.downloadDefaultExcelCallbacks(), "data"),
            Input(self.buttonDownloadDefaultExcelCallbacks(), "n_clicks"),
        )

    def download_button_pressed(self, export_nclicks):
        excel_manager = self.instanciateManagers()
        df = excel_manager.getDefaultExcel()
        return dcc.send_data_frame(
            df.to_excel,
            "default_recount_excel.xlsx",
            sheet_name="Sheet_name_1",
            # index=0, # TODO: remove index from excel
        )
